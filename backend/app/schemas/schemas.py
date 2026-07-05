from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class FeedbackItemSchema(BaseModel):
    id: int
    original_text: str
    sentiment: Optional[str]
    topics: Optional[List[str]]
    is_complaint: int
    is_feature_request: int
    priority_score: float

    class Config:
        from_attributes = True

class FeedbackBatchSchema(BaseModel):
    id: int
    filename: str
    upload_time: datetime
    status: str
    items: List[FeedbackItemSchema] = []

    class Config:
        from_attributes = True

class DashboardStatsResponse(BaseModel):
    total_feedback: int
    positive: int
    neutral: int
    negative: int
    top_complaints: List[Dict[str, Any]]
    trending_issues: List[Dict[str, Any]]
    sentiment_over_time: List[Dict[str, Any]]

class MemoryResponse(BaseModel):
    id: int
    batch_id: int
    created_at: datetime
    summary: str
    top_complaints: List[str]
    top_requests: List[str]
    sentiment_distribution: Dict[str, int]
    
    class Config:
        from_attributes = True

class RoutingLogResponse(BaseModel):
    id: int
    timestamp: datetime
    prompt_type: str
    model_selected: str
    reason: str
    latency_ms: float
    estimated_cost: float
    tokens_used: int
    status: str

    class Config:
        from_attributes = True
