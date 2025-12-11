import os
import numpy as np
import httpx
from langchain_openai import OpenAIEmbeddings

# Azure httpx client (SSL disabled per hackathon requirement)
client = httpx.Client(verify=False)

# Azure Embedding Model
emb = OpenAIEmbeddings(
    base_url="https://genailab.tcs.in",
    model="azure/genailab-maas-text-embedding-3-large",
    api_key=os.getenv("AZURE_API_KEY"),
    http_client=client
)


def heuristic_score_patch(patch, cluster_summary):
    """
    Your original deterministic scoring logic (kept exactly as-is).
    """
    score = 0

    explanation = patch["explanation"].lower()
    size = cluster_summary.get("size", 1)

    if "halluc" in explanation:
        score += 0.4
    if "factual" in explanation:
        score += 0.3

    clarity_bonus = max(0, 1 - len(patch["patched_prompt"]) / 2000)
    score += 0.1 * clarity_bonus

    severity = min(1.0, size / 50)
    score += 0.2 * severity

    return score


def semantic_score_patch(patch):
    """
    NEW: Semantic embedding-based score using Azure text embeddings.
    Higher vector magnitude = richer, stronger constraint language.
    This stabilizes ranking in Prompt-3 offline RL.
    """
    try:
        vec = emb.embed_query(patch["patched_prompt"])
        return float(np.linalg.norm(vec))
    except Exception as e:
        print("Embedding error:", e)
        return 0.0


def score_patch(patch, cluster_summary):
    """
    Combined final score = heuristic + semantic * weight.
    """
    h_score = heuristic_score_patch(patch, cluster_summary)
    s_score = semantic_score_patch(patch)

    # Weight semantic importance lightly for stability
    final_score = h_score + 0.1 * s_score
    return final_score


def rank_patches(patches, cluster_summary):
    """
    Returns list of dicts: {patch_id, score}
    Sorted descending by final combined score.
    """
    results = []

    for p in patches:
        score = score_patch(p, cluster_summary)
        results.append({
            "patch_id": p["patch_id"],
            "score": score
        })

    return sorted(results, key=lambda x: x["score"], reverse=True)
