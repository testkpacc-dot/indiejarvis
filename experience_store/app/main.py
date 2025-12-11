import json
from typing import List

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .db import get_db, init_db
from . import models, schemas

app = FastAPI(title="Experience Store Service", version="1.0.0")


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/health")
def health():
    return {"ok": True, "service": "experience_store"}


@app.post("/api/v1/log")
def log_experience(
    payload: schemas.ExperienceLogIn, db: Session = Depends(get_db)
):
    exp = models.Experience(
        context=json.dumps(payload.context),
        prompt_id=payload.prompt_id,
        response=json.dumps(payload.response),
        trace=payload.trace,
        verifier_result=json.dumps(payload.verifier_result),
        feedback=json.dumps(payload.feedback) if payload.feedback else None,
    )
    db.add(exp)
    db.commit()
    db.refresh(exp)
    return {"ok": True, "data": {"id": exp.id, "timestamp": exp.timestamp}}


@app.get("/api/v1/experiences", response_model=schemas.ExperiencesListResponse)
def list_experiences(
    db: Session = Depends(get_db),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    q = (
        db.query(models.Experience)
        .order_by(models.Experience.timestamp.desc())
        .offset(offset)
        .limit(limit)
    )
    rows: List[models.Experience] = q.all()

    items: List[schemas.ExperienceOut] = []
    for r in rows:
        items.append(
            schemas.ExperienceOut(
                id=r.id,
                timestamp=r.timestamp,
                context=json.loads(r.context),
                prompt_id=r.prompt_id,
                response=json.loads(r.response),
                trace=r.trace,
                verifier_result=json.loads(r.verifier_result),
                feedback=json.loads(r.feedback) if r.feedback else None,
            )
        )

    return schemas.ExperiencesListResponse(items=items)
