from unittest.mock import Mock, patch
import backend.rl_trainer.utils as utils

def test_fetch_experiences_handles_errors(monkeypatch):
    class BadResp:
        def raise_for_status(self): raise Exception("boom")
    monkeypatch.setattr("backend.rl_trainer.utils.requests.get", lambda *args, **kwargs: BadResp())
    exps = utils.fetch_experiences(limit=5)
    assert exps == []  # on error returns empty list

def test_verify_output_handles_failure(monkeypatch):
    class BadResp:
        def raise_for_status(self): raise Exception("boom")
    monkeypatch.setattr("backend.rl_trainer.utils.requests.post", lambda *args, **kwargs: BadResp())
    res = utils.verify_output("p1", {}, "out")
    assert isinstance(res, dict)
    assert res.get("reward", 0) == 0
