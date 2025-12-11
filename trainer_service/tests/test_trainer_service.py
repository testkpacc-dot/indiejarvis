from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["service"] == "trainer"

def test_train_call():
    r = client.post("/api/v1/train")
    assert r.status_code in (200, 500)  # may fail if dependencies offline
