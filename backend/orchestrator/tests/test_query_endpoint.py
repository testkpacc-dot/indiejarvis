import pytest
from fastapi.testclient import TestClient
import os
import sys
from pathlib import Path

# ensure package path
ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "app"))

os.environ["DEV_MOCK_MODE"] = "1"

from app.main import app  # noqa

client = TestClient(app)


def test_query_basic_success():
    payload = {
        "user_id": "u1",
        "session_id": "s1",
        "text": "Hello orchestrator",
        "features": {"risk": "low"}
    }
    r = client.post("/api/v1/query", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert body["ok"] is True
    data = body["data"]
    assert "response_text" in data
    assert "prompt_id" in data
    assert "verifier_result" in data


def test_query_missing_text():
    payload = {"user_id": "u1", "session_id": "s1"}
    r = client.post("/api/v1/query", json=payload)
    assert r.status_code == 422
