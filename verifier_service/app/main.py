# Main application entry point
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .db import SessionLocal, engine, Base
from .schemas import VerifyRequest, VerifyResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Verifier Service")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/api/v1/verify", response_model=VerifyResponse)
def verify(req: VerifyRequest, db: Session = Depends(get_db)):
    """
    Verify a response for hallucinations, PII, and rule violations
    """
    # Placeholder implementation
    return VerifyResponse(
        is_valid=True,
        issues=[],
        message="Response passed verification"
    )
