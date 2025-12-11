from fastapi import FastAPI
from . import schemas, rules

app = FastAPI(title="Verifier Service", version="1.0.0")


@app.get("/health")
def health():
    return {"ok": True, "service": "verifier"}


@app.post("/api/v1/verify", response_model=schemas.VerifierResult)
def verify(payload: schemas.VerifyRequest):
    result = rules.evaluate(
        prompt_id=payload.prompt_id,
        context=payload.context,
        response=payload.response,
    )
    return schemas.VerifierResult(**result)
