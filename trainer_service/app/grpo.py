import torch
import torch.nn.functional as F

def compute_rewards(batch):
    # batch is list of experience objects
    rewards = []
    for exp in batch:
        r = exp["verifier_result"]["reward"]
        rewards.append(float(r))
    return torch.tensor(rewards)

def compute_loss(policy_output, rewards, kl_penalty=0.01):
    # mock KL term (encourages staying close to baseline)
    baseline = torch.zeros_like(policy_output)
    mse = F.mse_loss(policy_output.squeeze(), rewards)
    kl = F.mse_loss(policy_output, baseline)
    return mse + kl_penalty * kl
