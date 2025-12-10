Prompt 3 — Offline Learning & Self-Improvement Pipeline

This module implements the Offline Intelligence Layer of our Agentic Adaptive-Prompt System.
It contains four independently running FastAPI microservices:

Failure Clustering Service

Patch Generator Service

Patch Ranker Service

RL Trainer Service (GRPO-based offline reinforcement learning)

These services operate entirely offline, consuming experience data and producing improved prompt versions.
They do not affect the real-time inference pipeline.

Architecture Overview
ExperienceStore
    ↓
FailureClustering ───► clusters + representative failures
    ↓
PatchGenerator ─────► N candidate prompt patches
    ↓
Ranker ─────────────► sorted patches (select top-1)
    ↓
RLTrainer (GRPO) ───► optimized prompt version
    ↓
PromptRegistry ─────► p_vX_Y.json

1. Failure Clustering Service (/api/v1/cluster)
Responsibilities

Pull failed interactions from ExperienceStore

TF-IDF encode failure responses

Perform KMeans clustering

Return cluster metadata + representative cases

Run
uvicorn backend.failure_clustering.main:app --port 8011 --reload

2. Patch Generator Service (/api/v1/generate-patches)
Responsibilities

Load existing prompt version

Generate 3–5 candidate improvements (template or LLM-assisted)

Output each candidate with explanation

Run
uvicorn backend.patch_generator.main:app --port 8012 --reload

3. Ranker Service (/api/v1/rank)
Responsibilities

Score patch candidates

Select the best one based on hallucination reduction, clarity, length safety, cluster severity

Run
uvicorn backend.ranker.main:app --port 8013 --reload

4. RL Trainer Service (/api/v1/train)
Responsibilities

Pull batches of experiences

Generate multiple candidate outputs

Evaluate with Verifier

Perform GRPO update

Write new prompt file to prompt_registry/

Run
uvicorn backend.rl_trainer.main:app --port 8014 --reload

Output Example (prompt_registry/p_v1_3.json)
{
  "prompt_id": "p_v1_3",
  "version": 3,
  "source": "rl_trainer",
  "text": "SYSTEM: Updated prompt ...",
  "metadata": {
    "created_at": "2025-12-10T14:22:00Z",
    "reward_gain": 0.12,
    "cluster_id": "cluster_1"
  }
}

Integration Summary for Judges

Prompt 3 ensures:

The system improves continuously

Hallucinations decrease over time

Prompts evolve safely using RL

Mistakes are clustered and addressed automatically

This closes the loop between experience → improvement → deployment.

END README.



 OFFLINE IMPROVEMENT PIPELINE (Prompt 3)
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│  ExperienceStore (historical interactions)                                 │
│             │                                                              │
│             ▼                                                              │
│  Failure Clustering Service ── groups similar failures                      │
│             │                                                              │
│             ▼                                                              │
│  Patch Generator Service ── proposes improved prompt versions               │
│             │                                                              │
│             ▼                                                              │
│  Ranker Service ── selects strongest candidate patch                        │
│             │                                                              │
│             ▼                                                              │
│  RL Trainer (GRPO) ── evaluates patch impact + improves prompt              │
│             │                                                              │
│             ▼                                                              │
│  PromptRegistry ── new version p_vX_Y.json stored                           │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘

Deployment Agent + Bandit Selector (Prompt 2) load new versions automatically.
This completes the system’s self-improving loop.