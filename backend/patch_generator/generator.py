import os
import httpx
from langchain_openai import ChatOpenAI

# Optional: Prompt Registry if needed later
PROMPT_REGISTRY_URL = os.getenv("PROMPT_REGISTRY_URL", "http://localhost:8002")

# Azure httpx client (SSL disabled per TCS infra requirement)
client = httpx.Client(verify=False)

# Azure MaaS DeepSeek LLM for patch generation
llm = ChatOpenAI(
    base_url="https://genailab.tcs.in",
    model="azure_ai/genailab-maas-DeepSeek-V3-0324",   # allowed model
    api_key=os.getenv("AZURE_API_KEY"),
    http_client=client,
    temperature=0.2
)

def llm_generated_patch(old_prompt: str, representative_samples):
    """
    Optional LLM-generated improvement based on failure samples.
    This supplements the rule-based patches.
    """
    failure_text = "\n".join(["- " + s for s in representative_samples])

    prompt = f"""
You are an expert LLM prompt engineer.

Improve the following prompt to reduce hallucinations, 
improve factual correctness, and handle uncertainty better.

CURRENT PROMPT:
{old_prompt}

OBSERVED FAILURE SAMPLES:
{failure_text}

Write ONLY the improved prompt. No explanation, no steps.
"""
    try:
        res = llm.invoke(prompt)
        return res.content
    except Exception as e:
        print("LLM generation failed:", e)
        return None


def generate_patches(old_prompt: str, representative_samples):
    """
    Returns a list of candidate patches:
    - Rule-based patches (deterministic)
    - One optional LLM-based patch
    """

    patches = []

    # -------------------------------
    # 1. Deterministic rule-based patches
    # -------------------------------
    patches.append({
        "patch_id": "patch_rule_01",
        "patched_prompt": old_prompt + "\n\nRULE: If uncertain, answer with 'I am not fully sure'.",
        "explanation": "Adds uncertainty handling."
    })

    patches.append({
        "patch_id": "patch_rule_02",
        "patched_prompt": old_prompt + "\n\nRULE: Provide factual grounding and cite only verified info.",
        "explanation": "Adds factual grounding requirement."
    })

    patches.append({
        "patch_id": "patch_rule_03",
        "patched_prompt": old_prompt + "\n\nRULE: Avoid hallucinations; do not invent information.",
        "explanation": "Reduces hallucinations."
    })

    # -------------------------------
    # 2. LLM-generated patch (optional)
    # -------------------------------
    improved = llm_generated_patch(old_prompt, representative_samples)
    if improved:
        patches.append({
            "patch_id": "patch_llm_01",
            "patched_prompt": improved,
            "explanation": "LLM-generated improvement using DeepSeek-V3."
        })

    return patches
