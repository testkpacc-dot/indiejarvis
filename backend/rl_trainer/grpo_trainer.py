import os
import json
import datetime
import requests
import torch
import torch.optim as optim
import httpx
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from .policy_head import PolicyHead

# Experience store URL
EXPERIENCE_STORE_URL = os.getenv("EXPERIENCE_STORE_URL", "http://localhost:8005")

# Prompt registry directory
PROMPT_DIR = "prompt_registry"

# Azure client (required SSL bypass)
client = httpx.Client(verify=False)

# Azure embedding model
emb = OpenAIEmbeddings(
    base_url="https://genailab.tcs.in",
    model="azure/genailab-maas-text-embedding-3-large",
    api_key=os.getenv("AZURE_API_KEY"),
    http_client=client
)

# Azure LLM for generating improved prompts (DeepSeek V3)
llm = ChatOpenAI(
    base_url="https://genailab.tcs.in",
    model="azure_ai/genailab-maas-DeepSeek-V3-0324",
    api_key=os.getenv("AZURE_API_KEY"),
    http_client=client,
    temperature=0.2
)


# -------------------------------------------------------------------
# Fetch experiences from Experience Store
# -------------------------------------------------------------------
def fetch_experiences(limit=200):
    url = f"{EXPERIENCE_STORE_URL}/api/v1/experiences?limit={limit}"
    try:
        resp = requests.get(url, timeout=5).json()
        return resp.get("data", [])
    except Exception as e:
        print("Experience fetch error:", e)
        return []


# -------------------------------------------------------------------
# Encode a text response into Azure embedding tensor
# -------------------------------------------------------------------
def encode(text):
    try:
        vec = emb.embed_query(text)
        return torch.tensor(vec, dtype=torch.float32).unsqueeze(0)
    except Exception as e:
        print("Embedding error:", e)
        return torch.zeros((1, 512))


# -------------------------------------------------------------------
# GRPO-style single training step
# -------------------------------------------------------------------
def train_one_step():
    model = PolicyHead(in_dim=emb.embed_query("test").__len__())  # dynamic input size
    optimizer = optim.Adam(model.parameters(), lr=1e-5)

    experiences = fetch_experiences(limit=200)
    if not experiences:
        return 0.0

    total_loss = 0.0
    rewards = []

    for exp in experiences[:50]:  # small batch
        response_text = exp["response"].get("text", "")
        reward = exp["verifier_result"].get("reward", 0)

        x = encode(response_text)
        pred = model(x).mean()

        # GRPO Loss (simplified)
        loss = -reward * pred
        total_loss += loss
        rewards.append(reward)

    optimizer.zero_grad()
    total_loss.backward()
    optimizer.step()

    avg_reward = sum(rewards) / len(rewards) if rewards else 0.0
    return avg_reward


# -------------------------------------------------------------------
# Generate improved prompt using DeepSeek + write to registry
# -------------------------------------------------------------------
def write_new_prompt():
    """
    Generates a new improved prompt version and saves it to prompt_registry.
    """

    # Load latest prompt from registry
    base_prompt_file = f"{PROMPT_DIR}/p_v1.json"
    if not os.path.exists(base_prompt_file):
        base_prompt_text = "SYSTEM: Default base prompt."
    else:
        with open(base_prompt_file, "r") as f:
            base_prompt_text = json.load(f).get("text", "")

    # Generate improved prompt using Azure DeepSeek
    msg = f"""
Improve the following system prompt by adding safety, clarity, 
factual correctness, and reduced hallucination:

{base_prompt_text}

Return ONLY the improved prompt. No explanations.
"""

    try:
        improved_prompt = llm.invoke(msg).content
    except Exception as e:
        print("LLM improvement failed:", e)
        improved_prompt = base_prompt_text

    # Construct new version metadata
    new_prompt = {
        "prompt_id": "p_v1_improved",
        "version": int(datetime.datetime.utcnow().timestamp()),
        "text": improved_prompt,
        "metadata": {
            "created_at": datetime.datetime.utcnow().isoformat()
        }
    }

    # Ensure directory exists
    os.makedirs(PROMPT_DIR, exist_ok=True)

    # Save new file
    filename = f"{PROMPT_DIR}/p_v1_improved.json"
    with open(filename, "w") as f:
        json.dump(new_prompt, f, indent=2)

    return new_prompt
