import torch
import torch.nn as nn

class PolicyHead(nn.Module):
    def __init__(self, input_dim=512, hidden=256):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(input_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, input_dim)
        )

    def forward(self, x):
        return self.model(x)
