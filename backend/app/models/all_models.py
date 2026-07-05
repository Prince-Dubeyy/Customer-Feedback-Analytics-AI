from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.database import Base

class FeedbackBatch(Base):
    __tablename__ = "feedback_batches"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    upload_time = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    status = Column(String, default="processing") # processing, completed, failed
    
    items = relationship("FeedbackItem", back_populates="batch", cascade="all, delete")
    memory = relationship("Memory", back_populates="batch", uselist=False)

class FeedbackItem(Base):
    __tablename__ = "feedback_items"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("feedback_batches.id"))
    original_text = Column(Text)
    
    # Analysis results
    sentiment = Column(String) # positive, negative, neutral
    topics = Column(JSON) # List of strings
    is_complaint = Column(Integer, default=0) # boolean
    is_feature_request = Column(Integer, default=0) # boolean
    priority_score = Column(Float, default=0.0)
    
    batch = relationship("FeedbackBatch", back_populates="items")

class Memory(Base):
    __tablename__ = "memories"
    
    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("feedback_batches.id"))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # The digested "Hindsight" memory representation of this batch
    summary = Column(Text)
    top_complaints = Column(JSON)
    top_requests = Column(JSON)
    sentiment_distribution = Column(JSON)
    
    batch = relationship("FeedbackBatch", back_populates="memory")

class RoutingLog(Base):
    __tablename__ = "routing_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    prompt_type = Column(String)
    model_selected = Column(String)
    reason = Column(String)
    latency_ms = Column(Float)
    estimated_cost = Column(Float)
    tokens_used = Column(Integer)
    status = Column(String) # success, fallback, failed
