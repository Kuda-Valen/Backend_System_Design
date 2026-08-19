from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from datetime import datetime

from .database import engine, Base, get_db
from .models import ExamCountdownModel

# Automatically create database tables on startup (For development/migration simplicity)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="StudeX - Tracker Microservice",
    description="Handles exam countdowns and micro-study tracking metrics with PostgreSQL.",
    version="1.0.0"
)

# --- PYDANTIC SCHEMAS ---
class ExamCountdownCreate(BaseModel):
    subject: str
    exam_date: datetime
    target_hours: float

class ExamCountdownResponse(ExamCountdownCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Allows Pydantic to read data directly from SQLAlchemy ORM models


# --- HEALTH CHECK ENDPOINT ---
@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "healthy", "service": "tracker-service", "database": "connected"}


# --- TRACKER ENDPOINTS ---
@app.post("/countdowns", response_model=ExamCountdownResponse, status_code=status.HTTP_201_CREATED)
async def create_countdown(payload: ExamCountdownCreate, db: Session = Depends(get_db)):
    """Persists a new exam countdown tracker directly to PostgreSQL."""
    db_item = ExamCountdownModel(
        subject=payload.subject,
        exam_date=payload.exam_date,
        target_hours=payload.target_hours
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.get("/countdowns", response_model=List[ExamCountdownResponse])
async def list_countdowns(db: Session = Depends(get_db)):
    """Retrieves all exam countdowns from PostgreSQL."""
    items = db.query(ExamCountdownModel).all()
    return items


@app.get("/countdowns/{countdown_id}", response_model=ExamCountdownResponse)
async def get_countdown(countdown_id: int, db: Session = Depends(get_db)):
    """Fetches a single exam countdown record from PostgreSQL by ID."""
    item = db.query(ExamCountdownModel).filter(ExamCountdownModel.id == countdown_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Countdown with ID {countdown_id} not found."
        )
    return item