from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.db.database import get_db
from app.models.all_models import FeedbackBatch, FeedbackItem, Memory, RoutingLog
from app.schemas.schemas import FeedbackBatchSchema, DashboardStatsResponse, MemoryResponse, RoutingLogResponse
from app.services.feedback_service import feedback_service
from app.core.hindsight import hindsight_engine

router = APIRouter()

@router.post("/reset")
def reset_database(db: Session = Depends(get_db)):
    db.query(FeedbackItem).delete()
    db.query(FeedbackBatch).delete()
    db.query(RoutingLog).delete()
    db.query(Memory).delete()
    db.commit()
    return {"status": "success", "message": "Database reset successfully."}

@router.post("/upload-feedback")
async def upload_feedback(
    file: UploadFile = None,
    text: str = Form(None),
    db: Session = Depends(get_db)
):
    if not file and not text:
        raise HTTPException(status_code=400, detail="Must provide either a file or text.")
        
    # Completely replace the current dataset
    reset_database(db)
        
    content = ""
    filename = "manual_text"
    
    if file:
        content_bytes = await file.read()
        content = content_bytes.decode('utf-8')
        filename = file.filename
    else:
        content = text
        
    batch_id, reflection = await feedback_service.process_feedback_csv(db, filename, content)
    
    return {
        "status": "success",
        "batch_id": batch_id,
        "reflection": reflection
    }

@router.get("/dashboard", response_model=DashboardStatsResponse)
def get_dashboard_stats(db: Session = Depends(get_db)):
    # Get the latest batch
    latest_batch = db.query(FeedbackBatch).order_by(desc(FeedbackBatch.id)).first()
    
    if not latest_batch:
        return DashboardStatsResponse(
            total_feedback=0, positive=0, neutral=0, negative=0,
            top_complaints=[], trending_issues=[], sentiment_over_time=[]
        )
        
    items = db.query(FeedbackItem).filter(FeedbackItem.batch_id == latest_batch.id).all()
    
    total = len(items)
    positive = 0
    neutral = 0
    negative = 0
    
    for item in items:
        sent = (item.sentiment or "neutral").lower().strip()
        if sent == 'positive':
            positive += 1
        elif sent == 'negative':
            negative += 1
        else:
            neutral += 1

    
    # Calculate top complaints for the latest batch
    complaints = {}
    for item in items:
        if item.is_complaint and item.topics:
            for t in item.topics:
                complaints[t] = complaints.get(t, 0) + 1
                
    top_complaints = [{"name": k, "value": v} for k, v in sorted(complaints.items(), key=lambda x: x[1], reverse=True)[:5]]
    
    # Calculate real trending issues by comparing with previous batch
    previous_batch = db.query(FeedbackBatch).filter(FeedbackBatch.id < latest_batch.id).order_by(desc(FeedbackBatch.id)).first()
    prev_complaints_counts = {}
    if previous_batch:
        prev_items = db.query(FeedbackItem).filter(FeedbackItem.batch_id == previous_batch.id).all()
        for item in prev_items:
            if item.is_complaint and item.topics:
                for t in item.topics:
                    prev_complaints_counts[t] = prev_complaints_counts.get(t, 0) + 1
                    
    trending_issues = []
    for tc in top_complaints:
        name = tc["name"]
        curr_val = tc["value"]
        prev_val = prev_complaints_counts.get(name, 0)
        
        if curr_val > prev_val:
            trend = "up"
        elif curr_val < prev_val:
            trend = "down"
        else:
            trend = "stable"
            
        trending_issues.append({"name": name, "trend": trend})

    return DashboardStatsResponse(
        total_feedback=total,
        positive=positive,
        neutral=neutral,
        negative=negative,
        top_complaints=top_complaints,
        trending_issues=trending_issues,
        sentiment_over_time=[] # To be populated if time-series data exists
    )

@router.get("/memory", response_model=list[MemoryResponse])
def get_memories(db: Session = Depends(get_db)):
    memories = db.query(Memory).order_by(desc(Memory.batch_id)).all()
    return memories

@router.get("/routing-log", response_model=list[RoutingLogResponse])
def get_routing_logs(db: Session = Depends(get_db)):
    logs = db.query(RoutingLog).order_by(desc(RoutingLog.id)).limit(100).all()
    return logs

@router.get("/report")
def generate_report(db: Session = Depends(get_db)):
    # Simulates an executive report using the latest memories
    memories = db.query(Memory).order_by(desc(Memory.batch_id)).limit(3).all()
    if not memories:
        return {"report": "Not enough data to generate report."}
        
    return {
        "report": "Executive Summary",
        "latest_insights": memories[0].summary if memories else "",
        "risks": memories[0].top_complaints if memories else [],
        "opportunities": memories[0].top_requests if memories else []
    }

@router.get("/model-stats")
def get_model_stats():
    import os
    import re
    # Path relative to backend/app/api/endpoints.py
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    report_path = os.path.join(base_dir, 'reports', 'model_performance.md')
    
    if not os.path.exists(report_path):
        return {"accuracy": "N/A", "precision": "N/A", "recall": "N/A", "f1": "N/A"}
        
    stats = {}
    with open(report_path, 'r') as f:
        content = f.read()
        
        acc_match = re.search(r'\*\*Accuracy\*\*:\s*([\d\.]+)', content)
        if acc_match: stats['accuracy'] = float(acc_match.group(1))
        
        prec_match = re.search(r'\*\*Precision \(weighted\)\*\*:\s*([\d\.]+)', content)
        if prec_match: stats['precision'] = float(prec_match.group(1))
        
        rec_match = re.search(r'\*\*Recall \(weighted\)\*\*:\s*([\d\.]+)', content)
        if rec_match: stats['recall'] = float(rec_match.group(1))
        
        f1_match = re.search(r'\*\*F1 Score \(weighted\)\*\*:\s*([\d\.]+)', content)
        if f1_match: stats['f1'] = float(f1_match.group(1))
        
    return stats
