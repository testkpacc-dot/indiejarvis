from fastapi import FastAPI
from .grpo_trainer import train_one_step, write_new_prompt   # FIXED relative import

app = FastAPI()

@app.post("/api/v1/train")
def train():
    avg_reward = train_one_step()
    new_prompt = write_new_prompt()
    return {"ok": True, "avg_reward": avg_reward, "new_prompt": new_prompt}

@app.get("/api/v1/health")
def health():
    return {"ok": True}
