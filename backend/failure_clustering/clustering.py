import requests
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from typing import List, Dict
import os

EXPERIENCE_STORE_URL = os.getenv("EXPERIENCE_STORE_URL", "http://localhost:8005")

def fetch_failed_experiences(limit: int = 500):
    url = f"{EXPERIENCE_STORE_URL}/api/v1/experiences?limit={limit}"
    resp = requests.get(url).json()
    data = resp["data"]

    failed = []
    for item in data:
        if item["verifier_result"].get("reward", 0) == 0:
            text = item["response"].get("text", "")
            if text.strip():
                failed.append({"id": item["id"], "text": text})

    return failed


def run_clustering(failed_samples: List[Dict], n_clusters: int = 3):
    texts = [x["text"] for x in failed_samples]
    if len(texts) < 2:
        return []

    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform(texts)

    kmeans = KMeans(n_clusters=min(n_clusters, len(texts)), random_state=42)
    labels = kmeans.fit_predict(X)

    clusters = {}
    for idx, label in enumerate(labels):
        clusters.setdefault(label, []).append(failed_samples[idx])

    results = []
    for label, items in clusters.items():
        results.append({
            "cluster_id": f"cluster_{label}",
            "size": len(items),
            "representative_samples": [x["id"] for x in items[:3]],
            "reason": "hallucination"
        })

    return results
