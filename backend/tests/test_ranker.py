from backend.ranker.ranker import rank_patches

def test_rank_patches_ordering():
    patches = [
        {"patch_id": "p1", "patched_prompt": "a"*10, "explanation": "reduces halluc"},
        {"patch_id": "p2", "patched_prompt": "b"*5000, "explanation": "factual improvement"},
        {"patch_id": "p3", "patched_prompt": "c"*100, "explanation": "minor change factual"}
    ]
    cluster_summary = {"size": 5}
    ranked = rank_patches(patches, cluster_summary)
    assert isinstance(ranked, list)
    assert all("patch_id" in r and "score" in r for r in ranked)
    # highest score should be first
    assert ranked[0]["score"] >= ranked[-1]["score"]
