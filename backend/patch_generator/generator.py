import os
import requests
import openai

PROMPT_REGISTRY_URL = os.getenv("PROMPT_REGISTRY_URL", "http://localhost:8002")
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_patches(old_prompt: str, representative_samples):
    patches = []

    patches.append({
        "patch_id": "patch_01",
        "patched_prompt": old_prompt + "\n\nRULE: If uncertain, answer with 'I am not fully sure'.",
        "explanation": "Adds uncertainty handling."
    })

    patches.append({
        "patch_id": "patch_02",
        "patched_prompt": old_prompt + "\n\nRULE: Provide factual grounding and cite only valid info.",
        "explanation": "Adds factual grounding requirement."
    })

    patches.append({
        "patch_id": "patch_03",
        "patched_prompt": old_prompt + "\n\nRULE: Avoid hallucinations; do not invent information.",
        "explanation": "Reduces hallucinations."
    })

    return patches
