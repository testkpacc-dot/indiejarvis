from fastapi.testclient import TestClient
import os
from app.main import app

client = TestClient(app)


def test_status_ok():
    r = client.get("/api/v1/status")
    assert r.status_code == 200
    body = r.json()
    assert "ok" in body and body["ok"] is True
    assert "services" in body
