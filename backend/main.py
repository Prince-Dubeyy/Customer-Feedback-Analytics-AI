import os
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import endpoints
from app.db.database import engine, Base

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ProductPulse AI API",
    description="Backend for Memory-Powered Customer Feedback Intelligence Agent",
    version="1.0.0"
)

# CORS configuration for production and local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://customer-feedback-analytics-ai.vercel.app", 
        "http://localhost:5173", 
        "http://localhost:5174", 
        "http://localhost:5175", 
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(endpoints.router, prefix="/api")

@app.get("/")
def root():
    return {
        "status": "healthy",
        "service": "AI-Powered Customer Feedback Analytics",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/info")
def info():
    return {
        "project": "AI-Powered Customer Feedback Analytics",
        "version": "1.0.0",
        "environment": "production"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
