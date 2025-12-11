import random
from datetime import datetime
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .db import get_db, init_db
from . import models, schemas

app = FastAPI(title="Bandit Selector Service", version="1.0.0")


@app.on_event("startup")
def on_startup():
    init_db()
    # Seed some default arms if table is empty
    db = next(get_db())
    if db.query(models.BanditArm).count() == 0:
        default_prompts = [
            ("p_v1_1", "low"),
            ("p_v1_2", "low"),
            ("p_v1_3", "high"),
        ]
        for pid, risk in default_prompts:
            db.add(
                models.BanditArm(
                    prompt_id=pid,
                    alpha=1,
                    beta=1,
                    samples=0,
                    risk=risk,
                )
            )
        db.commit()
        db.close()


@app.get("/health")
def health():
    return {"ok": True, "service": "bandit"}


def _sample_arm(arms: List[models.BanditArm]) -> models.BanditArm:
    """Thompson sampling: pick arm with highest Beta(alpha, beta) sample."""
    best_arm = None
    best_score = -1.0

    for arm in arms:
        score = random.betavariate(arm.alpha, arm.beta)
        if score > best_score:
            best_score = score
            best_arm = arm

    return best_arm


@app.post("/api/v1/choose", response_model=schemas.ChooseResponse)
def choose_arm(payload: schemas.ChooseRequest, db: Session = Depends(get_db)):
    # Determine risk from context features (default = low)
    risk = str(payload.context_features.get("risk", "low")).lower()

    q = db.query(models.BanditArm)
    if risk in ("low", "high"):
        q = q.filter(models.BanditArm.risk == risk)

    arms = q.all()
    if not arms:
        # fallback: any arm
        arms = db.query(models.BanditArm).all()

    if not arms:
        raise HTTPException(status_code=500, detail="No bandit arms configured")

    arm = _sample_arm(arms)
    return schemas.ChooseResponse(prompt_id=arm.prompt_id)


@app.post("/api/v1/reward")
def update_reward(payload: schemas.RewardRequest, db: Session = Depends(get_db)):
    arm = db.query(models.BanditArm).filter(
        models.BanditArm.prompt_id == payload.prompt_id
    ).first()

    if not arm:
        raise HTTPException(status_code=404, detail="Unknown prompt_id")

    if payload.reward not in (0, 1):
        raise HTTPException(status_code=400, detail="reward must be 0 or 1")

    if payload.reward == 1:
        arm.alpha += 1
    else:
        arm.beta += 1

    arm.samples += 1
    arm.last_update = datetime.utcnow()
    db.commit()
    db.refresh(arm)

    return {"ok": True}


@app.get("/api/v1/arms", response_model=schemas.ArmsListResponse)
def list_arms(db: Session = Depends(get_db)):
    arms = db.query(models.BanditArm).all()
    return {"arms": arms}
