import os
import json
import time
import httpx
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.all_models import RoutingLog
from groq import AsyncGroq
import asyncio

# cascadeflow - Runtime Intelligence & Model Routing Engine

# In a real startup, we'd have a budget DB table. For this demo, we simulate a budget.
class cascadeflowRouter:
    def __init__(self):
        self.api_key = os.environ.get("GROQ_API_KEY")
        self.client = AsyncGroq(api_key=self.api_key) if self.api_key else None
        
        # Primary routing configurations
        self.models = {
            "analysis": "llama-3.1-8b-instant", # Stable model for analysis
            "report": "llama-3.3-70b-versatile",# Using a capable model for reports
            "fallback": "llama-3.1-8b-instant"  # Valid fallback model
        }
        
        # We simulate budget constraints for the demo
        self.budget_remaining = float(os.environ.get("CASCADEFLOW_BUDGET", "5.00")) 

    def _log_request(self, db: Session, prompt_type: str, model: str, reason: str, latency: float, cost: float, tokens: int, status: str):
        log = RoutingLog(
            prompt_type=prompt_type,
            model_selected=model,
            reason=reason,
            latency_ms=latency,
            estimated_cost=cost,
            tokens_used=tokens,
            status=status
        )
        db.add(log)
        db.commit()

    async def execute_prompt(self, db: Session, prompt_type: str, system_prompt: str, user_prompt: str, db_lock: asyncio.Lock = None):
        start_time = time.time()
        
        # 1. Routing Logic
        if prompt_type == "report":
            model = self.models["report"]
            reason = "High reasoning required for executive reports."
            estimated_cost_per_1k = 0.0008
        else:
            model = self.models["analysis"]
            reason = "Standard analysis task, using optimal cost/performance model."
            estimated_cost_per_1k = 0.0003

        # 2. Budget Enforcement
        if self.budget_remaining < 0.01:
            model = self.models["fallback"]
            reason = "Budget constraint enforced. Downgraded to cheaper fallback model."
            estimated_cost_per_1k = 0.0001
            
        latency = 0.0
        cost = 0.0
        tokens = 0
        response_text = ""

        try:
            if not self.client:
                raise ValueError("GROQ_API_KEY not configured.")

            # 3. Execution with Groq
            chat_completion = await self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                model=model,
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            
            latency = (time.time() - start_time) * 1000
            tokens = chat_completion.usage.total_tokens
            cost = (tokens / 1000) * estimated_cost_per_1k
            self.budget_remaining -= cost
            
            response_text = chat_completion.choices[0].message.content
            print(f"[cascadeflow DEBUG] Raw Groq Response ({model}): {response_text}")
            status = "success"
            
        except Exception as e:
            # 4. Fallback / Error Handling
            latency = (time.time() - start_time) * 1000
            status = "failed"
            reason = f"Execution failed: {str(e)[:100]}"
            print(f"[cascadeflow ERROR] {e}")
            
            # Removed the mock fallback that automatically labels everything as neutral.
            # We explicitly return an error JSON object so the pipeline logs 'unknown' 
            # and doesn't silently hide the failure.
            response_text = json.dumps({
                "sentiment": "unknown",
                "topics": ["error"],
                "is_complaint": 0,
                "is_feature_request": 0,
                "priority_score": 0.0
            })

        # 5. Audit Logging
        if db_lock:
            async with db_lock:
                self._log_request(db, prompt_type, model, reason, latency, cost, tokens, status)
        else:
            self._log_request(db, prompt_type, model, reason, latency, cost, tokens, status)

        return json.loads(response_text)

router = cascadeflowRouter()
