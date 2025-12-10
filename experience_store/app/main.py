# Main application entry point
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from .db import SessionLocal, engine, Base
from .models import Experience
from .schemas import LogRequest, ExperienceRecord

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Experience Store Service")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/api/v1/log", response_model=dict)
def log_experience(req: LogRequest, db: Session = Depends(get_db)):
    """
    Log an experience record
    """
    experience = Experience(
        prompt_id=req.prompt_id,
        response=req.response,
        reward=req.reward,
        is_verified=req.is_verified,
        timestamp=datetime.utcnow()
    )
    db.add(experience)
    db.commit()
    db.refresh(experience)
    return {"ok": True, "id": experience.id}


@app.get("/api/v1/experiences", response_model=List[ExperienceRecord])
def get_experiences(db: Session = Depends(get_db)):
    """
    Retrieve all experience records
    """
    experiences = db.query(Experience).all()
    return experiences
