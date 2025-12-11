import torch
from torch.optim import Adam

from .policy_model import PolicyHead
from .data_loader import load_experiences
from .grpo import compute_rewards, compute_loss
from .prompt_writer import write_new_prompt_version
from .config import settings

async def run_training_cycle():
    # Load experience batch
    batch = await load_experiences(limit=settings.TRAIN_BATCH_SIZE)

    if not batch:
        return False, "No experience data available.", None

    # Create random feature vectors for hackathon
    x = torch.randn(len(batch), 16)

    # Compute reward tensor
    rewards = compute_rewards(batch)

    # Load or initialize policy model
    model = PolicyHead()
    optimizer = Adam(model.parameters(), lr=settings.LEARNING_RATE)

    # forward pass
    preds = model(x)

    # compute loss
    loss = compute_loss(preds, rewards, kl_penalty=settings.KL_TARGET)

    # backward
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    # Generate new prompt (simple heuristic)
    avg_reward = rewards.mean().item()
    new_prompt_text = f"SYSTEM: This is a trainer-enhanced prompt.\n# Average reward: {avg_reward}"

    # Version = number of experiences + 1
    new_version = len(batch) + 1

    new_prompt_id = await write_new_prompt_version(new_prompt_text, new_version)

    if not new_prompt_id:
        return False, "Failed to write new prompt version", None

    return True, "Training complete.", new_prompt_id
