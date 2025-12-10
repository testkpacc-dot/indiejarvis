def score_patch(patch, cluster_summary):
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

def rank_patches(patches, cluster_summary):
    return sorted(
        [{"patch_id": p["patch_id"], "score": score_patch(p, cluster_summary)}
         for p in patches],
        key=lambda x: x["score"],
        reverse=True
    )
