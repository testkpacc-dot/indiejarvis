import os
import requests
import numpy as np
from typing import List, Dict
from sklearn.cluster import KMeans
from langchain_openai import OpenAIEmbeddings
import httpx

# Experience Store URL
EXPERIENCE_STORE_URL = os.getenv("EXPERIENCE_STORE_URL", "http://localhost:8005")

# Azure httpx client (SSL disabled per TCS hackathon requirement)
client = httpx.Client(verify=False)

# Azure Embedding Model
emb = OpenAIEmbeddings(
    base_url="https://genailab.tcs.in",
    model="azure/genailab-maas-text-embedding-3-large",
    api_key=os.getenv("AZURE_API_KEY"),
    http_client=client
)


def fetch_failed_experiences(limit: int = 500):
    """
    Retrieves failed experiences (reward = 0) from Experience Store.
    """
    url = f"{EXPERIENCE_STORE_URL}/api/v1/experiences?limit={limit}"
    try:
        resp = requests.get(url, timeout=5).json()
    except Exception as e:
        print("Error fetching experiences:", e)
        return []

    data = resp.get("data", [])

    failed = []
    for item in data:
        vr = item.get("verifier_result", {})
        if vr.get("reward", 0) == 0:
            text = item.get("response", {}).get("text", "")
            if text.strip():
                failed.append({
                    "id": item["id"],
                    "text": text
                })

    return failed


def run_clustering(failed_samples: List[Dict], n_clusters: int = 3):
    """
    Clusters failed samples using Azure embeddings instead of TF-IDF.
    """
    if not failed_samples:
        return []

    texts = [x["text"] for x in failed_samples]

    # If not enough samples, return trivial structure
    if len(texts) <= 1:
        return [{
            "cluster_id": "cluster_0",
            "size": len(failed_samples),
            "representative_samples": [x["id"] for x in failed_samples],
            "reason": "hallucination"
        }]

    # === Azure Embedding Step ===
    try:
        vectors = emb.embed_documents(texts)  # returns list of embeddings
        vectors = np.array(vectors)
    except Exception as e:
        print("Embedding error:", e)
        return []

    # Fit KMeans (num clusters ≤ number of samples)
    k = min(n_clusters, len(failed_samples))
    kmeans = KMeans(n_clusters=k, n_init="auto", random_state=42)
    labels = kmeans.fit_predict(vectors)

    clusters = {}
    for idx, label in enumerate(labels):
        clusters.setdefault(label, []).append(failed_samples[idx])

    # Build output
    results = []
    for label, items in clusters.items():
        results.append({
            "cluster_id": f"cluster_{label}",
            "size": len(items),
            "representative_samples": [x["id"] for x in items[:3]],
            "reason": "hallucination"
        })

    return results
