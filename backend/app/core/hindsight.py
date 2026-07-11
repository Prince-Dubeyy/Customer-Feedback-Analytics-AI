import json
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.all_models import Memory, FeedbackBatch, FeedbackItem
from app.core.cascadeflow import router

# Hindsight - Persistent Memory & Temporal Comparison Engine

class HindsightEngine:
    async def retain(self, db: Session, batch_id: int):
        """Retain: Digest a processed batch and store it in long-term memory."""
        # 1. Gather all items in this batch
        items = db.query(FeedbackItem).filter(FeedbackItem.batch_id == batch_id).all()
        if not items:
            return None
            
        total = len(items)
        positive = 0
        neutral = 0
        negative = 0
        for i in items:
            sent = (i.sentiment or "neutral").lower().strip()
            if sent == "positive":
                positive += 1
            elif sent == "negative":
                negative += 1
            else:
                neutral += 1
        
        # Aggregate topics & complaints
        all_topics = {}
        for item in items:
            if item.topics:
                for t in item.topics:
                    all_topics[t] = all_topics.get(t, 0) + 1
                    
        # Sort topics
        sorted_topics = sorted(all_topics.items(), key=lambda x: x[1], reverse=True)
        top_complaints = [t[0] for t in sorted_topics if any(i.is_complaint for i in items if t[0] in (i.topics or []))][:5]
        top_requests = [t[0] for t in sorted_topics if any(i.is_feature_request for i in items if t[0] in (i.topics or []))][:5]
        
        # Create a summary narrative using cascadeflow
        system_prompt = "You are Hindsight, a memory engine. Summarize the key takeaways from this batch of customer feedback in 2-3 sentences. Output strictly JSON with key 'summary'."
        user_prompt = f"Total Feedback: {total}. Sentiment: Pos {positive}, Neu {neutral}, Neg {negative}. Top Complaints: {top_complaints}. Top Requests: {top_requests}."
        
        response = await router.execute_prompt(db, "report", system_prompt, user_prompt)
        summary_text = response.get("summary", "Summary generation failed.")
        
        # Store in Memory
        memory = Memory(
            batch_id=batch_id,
            summary=summary_text,
            top_complaints=top_complaints,
            top_requests=top_requests,
            sentiment_distribution={"positive": positive, "neutral": neutral, "negative": negative}
        )
        db.add(memory)
        db.commit()
        return memory

    async def reflect(self, db: Session, current_batch_id: int):
        """Reflect: Compare current batch with the immediate previous batch in memory to find trends."""
        # Get current memory
        current_memory = db.query(Memory).filter(Memory.batch_id == current_batch_id).first()
        if not current_memory:
            return {"trend_analysis": "No current memory found to reflect on."}
            
        # Recall previous memory
        previous_memory = db.query(Memory).filter(Memory.batch_id < current_batch_id).order_by(desc(Memory.batch_id)).first()
        
        if not previous_memory:
            return {"trend_analysis": "This is the first batch. No historical data to compare."}
            
        # Use cascadeflow to generate reflection
        system_prompt = "You are Hindsight Reflect. Compare the previous memory to the current memory. Highlight emerging trends, what improved, and what got worse (e.g. 'Checkout complaints increased'). Output strictly JSON with key 'trend_analysis' containing a string of 3-4 sentences."
        
        user_prompt = json.dumps({
            "previous_memory": {
                "summary": previous_memory.summary,
                "top_complaints": previous_memory.top_complaints,
                "sentiment": previous_memory.sentiment_distribution
            },
            "current_memory": {
                "summary": current_memory.summary,
                "top_complaints": current_memory.top_complaints,
                "sentiment": current_memory.sentiment_distribution
            }
        })
        
        response = await router.execute_prompt(db, "report", system_prompt, user_prompt)
        return response

hindsight_engine = HindsightEngine()
