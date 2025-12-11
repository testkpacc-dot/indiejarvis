import json
from unittest.mock import patch, Mock
import backend.failure_clustering.clustering as clustering

SAMPLE_RESPONSE = {
    "data": [
        {"id": "1", "verifier_result": {"reward": 0}, "response": {"text": "foo failed"}},
        {"id": "2", "verifier_result": {"reward": 1}, "response": {"text": "ok"}},
        {"id": "3", "verifier_result": {"reward": 0}, "response": {"text": "bar failed"}},
        {"id": "4", "verifier_result": {"reward": 0}, "response": {"text": "another fail"}}
    ]
}

def test_fetch_failed_experiences_returns_failed_only(monkeypatch):
    mock_resp = Mock()
    mock_resp.json.return_value = SAMPLE_RESPONSE
    mock_resp.raise_for_status = lambda: None

    monkeypatch.setattr("backend.failure_clustering.clustering.requests.get", lambda url, timeout=10: mock_resp)

    failed = clustering.fetch_failed_experiences(limit=10)
    ids = [f["id"] for f in failed]
    assert "1" in ids and "3" in ids and "4" in ids
    assert all(isinstance(f["text"], str) for f in failed)

def test_run_clustering_produces_clusters():
    samples = [
        {"id": "1", "text": "error connecting to database"},
        {"id": "2", "text": "cannot connect to db"},
        {"id": "3", "text": "UI shows wrong value"},
        {"id": "4", "text": "display shows wrong number"}
    ]
    clusters = clustering.run_clustering(samples, n_clusters=2)
    assert isinstance(clusters, list)
    assert all("cluster_id" in c and "size" in c for c in clusters)
