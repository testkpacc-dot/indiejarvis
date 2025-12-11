from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

from .db import get_db, engine, Base
from .models import Prompt
from .schemas import PromptIn, PromptOut, ListPromptsResponse, PromptListItem
from .storage import save_prompt_file
from .config import settings

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Prompt Registry Service", version="1.0.0")

@app.get("/health")
def health():
    return {"ok": True, "service": "prompt_registry"}


@app.post("/api/v1/prompt", status_code=201)
def create_prompt(payload: PromptIn, db: Session = Depends(get_db)):
    existing = db.query(Prompt).filter(Prompt.prompt_id == payload.prompt_id).order_by(Prompt.version.desc()).first()

    if existing:
        if payload.version is None or payload.version <= existing.version:
            raise HTTPException(
                status_code=400,
                detail=f"prompt_id exists with version {existing.version}. Provide higher version."
            )

    file_payload = {
        "prompt_id": payload.prompt_id,
        "version": payload.version,
        "text": payload.text,
        "meta_json": payload.meta_json,
    }

    file_path = save_prompt_file(payload.prompt_id, file_payload)

    p = Prompt(
        prompt_id=payload.prompt_id,
        version=payload.version,
        text=payload.text,
        meta_json=payload.meta_json,
        file_path=file_path,
    )

    db.add(p)
    db.commit()
    db.refresh(p)

    return {"ok": True, "data": PromptOut.model_validate(p).model_dump()}


@app.get("/api/v1/prompt/{prompt_id}", response_model=PromptOut)
def get_prompt(prompt_id: str, db: Session = Depends(get_db)):
    p = db.query(Prompt).filter(Prompt.prompt_id == prompt_id).order_by(Prompt.version.desc()).first()
    if not p:
        raise HTTPException(status_code=404, detail="prompt not found")
    return PromptOut.model_validate(p)


@app.get("/api/v1/prompts", response_model=ListPromptsResponse)
def list_prompts(db: Session = Depends(get_db)):
    rows = db.query(Prompt).order_by(Prompt.prompt_id, Prompt.version.desc()).all()
    seen = set()
    items = []

    for r in rows:
        if r.prompt_id in seen:
            continue
        seen.add(r.prompt_id)
        items.append(PromptListItem(
            prompt_id=r.prompt_id,
            version=r.version,
            meta_json=r.meta_json or {}
        ))

    return ListPromptsResponse(items=items)
