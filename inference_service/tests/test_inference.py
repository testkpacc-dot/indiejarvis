from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["service"] == "inference"

def test_generate_mock():
    payload = {
        "prompt_text": "SYSTEM: You are helpful.\nUSER: Hello",
        "context": {"features": {"user_query": "Hello"}}
    }
    r = client.post("/api/v1/generate", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "response_text" in data
    assert "PROMPT USED" in data["response_text"]
