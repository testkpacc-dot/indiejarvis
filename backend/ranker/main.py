from fastapi import FastAPI
from pydantic import BaseModel
from ranker import rank_patches

app = FastAPI()

class RankReq(BaseModel):
    patch_candidates: list
    cluster_summary: dict

@app.post("/api/v1/rank")
def rank(req: RankReq):
    ranked = rank_patches(req.patch_candidates, req.cluster_summary)
    return {"ok": True, "data": ranked}

@app.get("/api/v1/health")
def health():
    return {"ok": True}
