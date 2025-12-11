from fastapi import FastAPI
from pydantic import BaseModel
from .clustering import fetch_failed_experiences, run_clustering

app = FastAPI()

class ClusterRequest(BaseModel):
    limit: int = 200

@app.post("/api/v1/cluster")
def cluster(req: ClusterRequest):
    failed = fetch_failed_experiences(req.limit)
    clusters = run_clustering(failed)
    return {"ok": True, "data": clusters}

@app.get("/api/v1/health")
def health():
    return {"ok": True}
