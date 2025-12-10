# Main application entry point
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import random

from .db import SessionLocal, engine, Base
from .models import BanditArm
from .schemas import ChooseRequest, ChooseResponse, RewardRequest, ArmInfo

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bandit Selector Service")

MIN_SAMPLES_LOW_RISK = 50
MIN_SAMPLES_HIGH_RISK = 250


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/api/v1/arms", response_model=List[ArmInfo])
def list_arms(db: Session = Depends(get_db)):
    arms = db.query(BanditArm).all()
    return arms


@app.post("/api/v1/choose", response_model=ChooseResponse)
def choose_arm(req: ChooseRequest, db: Session = Depends(get_db)):
    arms = db.query(BanditArm).all()
    if not arms:
        raise HTTPException(status_code=400, detail="No arms configured")

    # Separate low-sampled arms by risk
    low_sample_arms = []
    for arm in arms:
        min_samples = (
            MIN_SAMPLES_HIGH_RISK if arm.risk == "high" else MIN_SAMPLES_LOW_RISK
        )
        if arm.samples < min_samples:
            low_sample_arms.append(arm)

    # If any arm is under min samples → explore among them
    candidate_arms = low_sample_arms if low_sample_arms else arms

    # Thompson Sampling with Beta(alpha, beta)
    best_arm = None
    best_sample = -1.0
    for arm in candidate_arms:
        sample = random.betavariate(arm.alpha, arm.beta)
        if sample > best_sample:
            best_sample = sample
            best_arm = arm

    if not best_arm:
        raise HTTPException(status_code=500, detail="Failed to select arm")

    return ChooseResponse(prompt_id=best_arm.prompt_id)


@app.post("/api/v1/reward")
def update_reward(req: RewardRequest, db: Session = Depends(get_db)):
    if req.reward not in (0, 1):
        raise HTTPException(status_code=400, detail="Reward must be 0 or 1")

    arm = db.query(BanditArm).filter(BanditArm.prompt_id == req.prompt_id).first()
    if not arm:
        raise HTTPException(status_code=404, detail="Prompt arm not found")

    if req.reward == 1:
        arm.alpha += 1
    else:
        arm.beta += 1

    arm.samples += 1
    arm.last_update = datetime.utcnow()

    db.add(arm)
    db.commit()
    db.refresh(arm)

    return {"ok": True}
