from fastapi import FastAPI
from .trainer import run_training_cycle
from .schemas import TrainResponse

app = FastAPI(title="Trainer Service", version="1.0.0")

@app.get("/health")
def health():
    return {"ok": True, "service": "trainer"}

@app.post("/api/v1/train", response_model=TrainResponse)
async def train():
    ok, msg, new_prompt_id = await run_training_cycle()
    return TrainResponse(ok=ok, message=msg, new_prompt_id=new_prompt_id)
