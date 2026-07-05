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
        lines = []
        try:
            # Try parsing as CSV first
            f = StringIO(content)
            reader = csv.DictReader(f)
            if reader.fieldnames and 'text' in [fn.lower() for fn in reader.fieldnames]:
                text_col = next(fn for fn in reader.fieldnames if fn.lower() == 'text')
                lines = [row[text_col] for row in reader if row.get(text_col)]
            else:
                # Fallback to line by line
                lines = [line.strip() for line in content.split('\n') if line.strip()]
        except Exception:
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            
        system_prompt = """You are an expert customer feedback analyzer. 
Analyze the provided feedback and return strictly a JSON object with:
- "sentiment": "positive", "negative", or "neutral" (feature requests should be classified as "neutral" unless explicitly positive or negative)
- "topics": list of strings (1-3 key topics, e.g. "checkout", "UI", "pricing")
- "is_complaint": 1 if complaint, 0 otherwise
- "is_feature_request": 1 if asking for a feature, 0 otherwise
- "priority_score": float between 0.0 and 10.0 indicating urgency"""

        # Prepare concurrency
        sem = asyncio.Semaphore(10)
        db_lock = asyncio.Lock()

        async def process_single(text: str):
            async with sem:
                # Use cascadeflow for analysis
                analysis = await router.execute_prompt(db, "analysis", system_prompt, text, db_lock=db_lock)
                
                # Parse sentiment safely
                raw_sentiment = str(analysis.get("sentiment", "unknown")).lower().strip()
                
                # Ensure it's one of the expected values, otherwise map to unknown
                if raw_sentiment not in ["positive", "negative", "neutral"]:
                    print(f"[FeedbackService DEBUG] Invalid sentiment '{raw_sentiment}', defaulting to 'unknown'.")
                    raw_sentiment = "unknown"
                
                print(f"[FeedbackService DEBUG] Extracted Sentiment: {raw_sentiment} | Is Complaint: {analysis.get('is_complaint')} | Topics: {analysis.get('topics')}")

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

        tasks = [process_single(text) for text in lines if text]
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
