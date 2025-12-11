from fastapi import FastAPI
from app.routers import query as query_router
from app.routers import health as health_router

app = FastAPI(title="Orchestrator", version="1.0")

app.include_router(health_router.router, prefix="/api/v1")
app.include_router(query_router.router, prefix="/api/v1")
