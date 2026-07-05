import asyncio
import os
import json
from dotenv import load_dotenv
load_dotenv('.env')

from app.core.cascadeflow import router
from app.db.database import SessionLocal

async def test():
    db = SessionLocal()
    router.models['fallback'] = 'llama3-70b-8192'
    router.budget_remaining = 0
    prompt = """You are an expert customer feedback analyzer. 
Analyze the provided feedback and return strictly a JSON object with:
- "sentiment": "positive", "negative", or "neutral"
- "topics": list of strings (1-3 key topics, e.g. "checkout", "UI", "pricing")
- "is_complaint": 1 if complaint, 0 otherwise
- "is_feature_request": 1 if asking for a feature, 0 otherwise
- "priority_score": float between 0.0 and 10.0 indicating urgency"""

    res = await router.execute_prompt(db, 'analysis', prompt, 'Checkout keeps failing.')
    print("RESULT:", res)

asyncio.run(test())
