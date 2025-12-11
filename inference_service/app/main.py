from fastapi import FastAPI, HTTPException
from .schemas import GenerateRequest, GenerateResponse
from .llm import run_llm
from .utils import create_request_id

app = FastAPI(title="Inference Service", version="1.0.0")

@app.get("/health")
def health():
    return {"ok": True, "service": "inference"}


@app.post("/api/v1/generate", response_model=GenerateResponse)
def generate(body: GenerateRequest):
    try:
        output = run_llm(body.prompt_text, body.context)
        return GenerateResponse(**output)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
