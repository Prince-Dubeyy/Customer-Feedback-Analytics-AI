import csv
from io import StringIO
from sqlalchemy.orm import Session
from app.models.all_models import FeedbackBatch, FeedbackItem
from app.core.cascadeflow import router
from app.core.hindsight import hindsight_engine
import asyncio

class FeedbackService:
    async def process_feedback_csv(self, db: Session, filename: str, content: str):
        # Create a new batch
        batch = FeedbackBatch(filename=filename, status="processing")
        db.add(batch)
        db.commit()
        db.refresh(batch)
        
        # Parse CSV or Text lines
        records = []
        try:
            # Try parsing as CSV first
            f = StringIO(content)
            reader = csv.DictReader(f)
            if reader.fieldnames and 'text' in [fn.lower() for fn in reader.fieldnames]:
                text_col = next(fn for fn in reader.fieldnames if fn.lower() == 'text')
                
                # Check for sentiment column
                sentiment_col = None
                if 'sentiment' in [fn.lower() for fn in reader.fieldnames]:
                    sentiment_col = next(fn for fn in reader.fieldnames if fn.lower() == 'sentiment')

                for row in reader:
                    text_val = row.get(text_col)
                    if text_val and text_val.strip():
                        record = {"text": text_val.strip()}
                        if sentiment_col and row.get(sentiment_col):
                            record["sentiment"] = row.get(sentiment_col).strip().lower()
                        records.append(record)
            else:
                # Fallback to line by line
                records = [{"text": line.strip()} for line in content.split('\n') if line.strip()]
        except Exception:
            records = [{"text": line.strip()} for line in content.split('\n') if line.strip()]
            
        system_prompt = """You are an expert customer feedback analyzer. 
Analyze the provided feedback and return strictly a JSON object with:
- "topics": list of strings (1-3 key topics, e.g. "checkout", "UI", "pricing")
- "is_complaint": 1 if complaint, 0 otherwise
- "is_feature_request": 1 if asking for a feature, 0 otherwise
- "priority_score": float between 0.0 and 10.0 indicating urgency"""

        # Prepare concurrency
        sem = asyncio.Semaphore(10)
        db_lock = asyncio.Lock()

        async def process_single(record: dict):
            text = record["text"]
            async with sem:
                # 1. Use Pre-labelled Sentiment or Fallback to ML Model
                raw_sentiment = record.get("sentiment")
                if not raw_sentiment or raw_sentiment not in ['positive', 'negative', 'neutral']:
                    from app.services.ml_service import ml_service
                    raw_sentiment = ml_service.predict_sentiment(text)
                
                # 2. LLM for Deep Analysis (topics, complaints, features)
                analysis = await router.execute_prompt(db, "analysis", system_prompt, text, db_lock=db_lock)
                
                print(f"[FeedbackService DEBUG] ML Sentiment: {raw_sentiment} | Is Complaint: {analysis.get('is_complaint')} | Topics: {analysis.get('topics')}")

                async with db_lock:
                    item = FeedbackItem(
                        batch_id=batch.id,
                        original_text=text,
                        sentiment=raw_sentiment,
                        topics=analysis.get("topics", []),
                        is_complaint=int(analysis.get("is_complaint", 0)),
                        is_feature_request=int(analysis.get("is_feature_request", 0)),
                        priority_score=float(analysis.get("priority_score", 0.0))
                    )
                    db.add(item)

        tasks = [process_single(rec) for rec in records]
        if tasks:
            await asyncio.gather(*tasks)
            
        # Complete batch
        batch.status = "completed"
        db.commit()
        
        # Trigger Hindsight (Retain & Reflect)
        await hindsight_engine.retain(db, batch.id)
        reflection = await hindsight_engine.reflect(db, batch.id)
        
        return batch.id, reflection

feedback_service = FeedbackService()
