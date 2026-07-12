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
            
            # Robustly detect text column
            text_col = None
            if reader.fieldnames:
                for col in reader.fieldnames:
                    if col.lower().strip() in ['text', 'review', 'content', 'feedback', 'message']:
                        text_col = col
                        break
                        
            if text_col:
                # Robustly detect sentiment column
                sentiment_col = None
                for col in reader.fieldnames:
                    if col.lower().strip() in ['sentiment', 'label', 'rating', 'class']:
                        sentiment_col = col
                        break

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
Analyze the provided feedback text and return strictly a JSON object with:
- "topics": list of strings (1-3 key topics derived DIRECTLY from the text, e.g. "checkout", "UI", "pricing"). Do not use generic categories.
- "is_complaint": 1 if the user is complaining about an issue, 0 otherwise
- "is_feature_request": 1 if asking for a feature, 0 otherwise
- "priority_score": float between 0.0 and 10.0 indicating urgency"""

        # Prepare concurrency
        sem = asyncio.Semaphore(10)
        db_lock = asyncio.Lock()

        async def process_single(record: dict):
            text = record["text"]
            async with sem:
                # 1. Mode A vs Mode B
                raw_sentiment = record.get("sentiment")
                
                # Normalize sentiment mapping if user uploaded numeric ratings, etc.
                if raw_sentiment in ['pos', '1']: raw_sentiment = 'positive'
                elif raw_sentiment in ['neg', '0']: raw_sentiment = 'negative'
                elif raw_sentiment in ['neu', '2', 'none']: raw_sentiment = 'neutral'
                confidence = 0.0
                if raw_sentiment and raw_sentiment in ['positive', 'negative', 'neutral']:
                    # Mode A: Labeled Dataset Mode (Ground Truth)
                    confidence = 1.0 # 100% confidence for ground truth
                else:
                    # Mode B: Prediction Mode
                    try:
                        from app.services.ml_service import ml_service
                        raw_sentiment, confidence = ml_service.predict_sentiment(text)
                    except Exception as e:
                        print(f"ML prediction failed: {e}")
                        raw_sentiment = 'neutral' # safe fallback
                        confidence = 0.0
                
                # 2. LLM for Deep Analysis (topics, complaints, features)
                analysis = await router.execute_prompt(db, "analysis", system_prompt, text, db_lock=db_lock)
                
                print(f"[FeedbackService DEBUG] Final Sentiment: {raw_sentiment} (conf: {confidence:.2f}) | Is Complaint: {analysis.get('is_complaint')} | Topics: {analysis.get('topics')}")

                async with db_lock:
                    item = FeedbackItem(
                        batch_id=batch.id,
                        original_text=text,
                        sentiment=raw_sentiment,
                        sentiment_confidence=confidence,
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
