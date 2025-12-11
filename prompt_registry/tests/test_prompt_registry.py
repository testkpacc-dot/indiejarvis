import os
import json
import tempfile
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db import Base, get_db
from app.models import Prompt

# in-memory DB
TEST_DB = "sqlite:///:memory:"
engine = create_engine(TEST_DB, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["ok"] is True

def test_create_and_get_prompt(tmp_path):
    # override prompts dir via env if needed
    payload = {
        "prompt_id": "p_v1_test",
        "version": 1,
        "text": "SYSTEM: You are helpful.\nUSER: Hello",
        "metadata": {"risk": "low"}
    }
    r = client.post("/api/v1/prompt", json=payload)
    assert r.status_code == 201
    body = r.json()
    assert body["ok"] is True
    assert body["data"]["prompt_id"] == "p_v1_test"

    # get prompt
    r2 = client.get("/api/v1/prompt/p_v1_test")
    assert r2.status_code == 200
    got = r2.json()
    assert got["prompt_id"] == "p_v1_test"
    assert "SYSTEM" in got["text"] or "USER" in got["text"]

def test_list_prompts():
    # create second prompt
    payload = {
        "prompt_id": "p_v1_test2",
        "version": 1,
        "text": "text 2",
        "metadata": {"risk": "low"}
    }
    client.post("/api/v1/prompt", json=payload)
    r = client.get("/api/v1/prompts")
    assert r.status_code == 200
    data = r.json()
    assert "items" in data
    assert any(it["prompt_id"] == "p_v1_test2" for it in data["items"])
