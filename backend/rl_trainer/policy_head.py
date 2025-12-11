import torch
import torch.nn as nn

class PolicyHead(nn.Module):
    """
    A small feed-forward policy head used for GRPO-style optimization.
    Input dimension = Azure embedding dimension.
    Output = single scalar score predicting expected reward.
    """

    def __init__(self, in_dim, hidden=256):
        super().__init__()

        self.net = nn.Sequential(
            nn.Linear(in_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, 1)  # Output is a single reward estimate
        )

    def forward(self, x):
        return self.net(x)
