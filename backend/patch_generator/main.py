from fastapi import FastAPI
from pydantic import BaseModel
from backend.patch_generator.generator import generate_patches


app = FastAPI()

class PatchReq(BaseModel):
    old_prompt: str
    representative_samples: list

@app.post("/api/v1/generate-patches")
def gen(req: PatchReq):
    patches = generate_patches(req.old_prompt, req.representative_samples)
    return {"ok": True, "data": patches}

@app.get("/api/v1/health")
def health():
    return {"ok": True}
