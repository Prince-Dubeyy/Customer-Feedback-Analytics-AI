import asyncio
import httpx
from app.db.database import SessionLocal, engine, Base
from app.models.all_models import FeedbackBatch, FeedbackItem
from app.api.endpoints import get_dashboard_stats

csv_content = """text,sentiment
"The checkout process is terrible.",negative
"I love the new design!",positive
"It's okay, nothing special.",neutral
"I couldn't find the search bar.",negative
"""

async def test():
    # Write to a temp file
    with open("temp_test.csv", "w") as f:
        f.write(csv_content)
        
    print("Testing upload...")
    async with httpx.AsyncClient(app=None, base_url="http://127.0.0.1:8000") as client:
        # Actually I can just call the service directly without httpx
        pass

# Call the service directly
import sys
import os
sys.path.append(os.path.abspath('.'))

from app.services.feedback_service import feedback_service
from app.api.endpoints import reset_database

async def direct_test():
    db = SessionLocal()
    print("Resetting DB...")
    reset_database(db)
    
    print("Uploading CSV...")
    batch_id, reflection = await feedback_service.process_feedback_csv(db, "test.csv", csv_content)
    
    print("Batch ID:", batch_id)
    items = db.query(FeedbackItem).all()
    for item in items:
        print(f"[{item.sentiment}] {item.original_text}")
        
    from app.api.endpoints import get_dashboard_stats
    stats = get_dashboard_stats(db)
    print("Stats:")
    print(f"Total: {stats.total_feedback}, Pos: {stats.positive}, Neu: {stats.neutral}, Neg: {stats.negative}")
    
    db.close()

if __name__ == "__main__":
    asyncio.run(direct_test())
