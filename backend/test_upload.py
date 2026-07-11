import asyncio
import sys
import os

sys.path.append(os.path.abspath('.'))

from app.db.database import SessionLocal
from app.models.all_models import FeedbackItem
from app.services.feedback_service import feedback_service
from app.api.endpoints import reset_database
from app.api.endpoints import get_dashboard_stats

async def direct_test():
    db = SessionLocal()
    
    # TEST MODE A (Labeled Dataset)
    print("="*50)
    print("TESTING MODE A: LABELED DATASET")
    print("="*50)
    reset_database(db)
    
    with open("test_labeled_dataset.csv", "r", encoding="utf-8") as f:
        csv_content = f.read()
        
    await feedback_service.process_feedback_csv(db, "test_labeled_dataset.csv", csv_content)
    
    stats_a = get_dashboard_stats(db)
    print(f"Total: {stats_a.total_feedback}, Pos: {stats_a.positive}, Neu: {stats_a.neutral}, Neg: {stats_a.negative}")
    assert stats_a.total_feedback == 60
    assert stats_a.positive == 20
    assert stats_a.neutral == 20
    assert stats_a.negative == 20
    print("MODE A PASSED!\n")

    # TEST MODE B (Unlabeled Dataset)
    print("="*50)
    print("TESTING MODE B: PREDICTION DATASET")
    print("="*50)
    reset_database(db)
    
    with open("test_unlabeled_dataset.csv", "r", encoding="utf-8") as f:
        csv_content = f.read()
        
    await feedback_service.process_feedback_csv(db, "test_unlabeled_dataset.csv", csv_content)
    
    stats_b = get_dashboard_stats(db)
    print(f"Total: {stats_b.total_feedback}, Pos: {stats_b.positive}, Neu: {stats_b.neutral}, Neg: {stats_b.negative}")
    assert stats_b.total_feedback == 60
    assert (stats_b.positive + stats_b.neutral + stats_b.negative) == 60
    print("MODE B PASSED!\n")

    db.close()

if __name__ == "__main__":
    asyncio.run(direct_test())
