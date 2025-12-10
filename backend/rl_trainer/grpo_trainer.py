import torch
import torch.optim as optim
from policy_head import PolicyHead
from utils import fetch_experiences, verify_output
import json
import os
import datetime

PROMPT_DIR = "prompt_registry"

def train_one_step():
    model = PolicyHead()
    opt = optim.Adam(model.parameters(), lr=1e-5)

    experiences = fetch_experiences()
    rewards = []
    loss = 0

    for exp in experiences[:50]:
        x = torch.randn(1, 512)
        output = model(x)

        new_output = "Improved: " + exp["response"]["text"]
        verification = verify_output(exp["prompt_id"], exp["context"], new_output)

        reward = verification["reward"]
        rewards.append(reward)
        loss += -reward * output.mean()

    opt.zero_grad()
    loss.backward()
    opt.step()

    return sum(rewards) / len(rewards)

def write_new_prompt():
    new_prompt = {
        "prompt_id": "p_v1_new",
        "version": 99,
        "text": "SYSTEM: Improved by RL Trainer.",
        "metadata": {
            "created_at": datetime.datetime.utcnow().isoformat()
        }
    }
    os.makedirs(PROMPT_DIR, exist_ok=True)
    with open(f"{PROMPT_DIR}/p_v1_new.json", "w") as f:
        json.dump(new_prompt, f, indent=2)

    return new_prompt
