"""Small 1-D CNN demonstration on SYNTHETIC waveforms, not real ECGs."""
import argparse
import numpy as np
import torch
from torch import nn

def synthetic(n=400, length=128, seed=42):
    rng = np.random.default_rng(seed)
    t = np.linspace(0, 1, length)
    labels = rng.integers(0, 2, size=n)
    signals = []
    for y in labels:
        freq = 6 if y == 0 else 11
        wave = np.sin(2 * np.pi * freq * t)
        wave += (0.15 if y else 0.0) * np.sin(2 * np.pi * 19 * t)
        wave += rng.normal(0, 0.18, length)
        signals.append(wave.astype(np.float32))
    return torch.tensor(np.array(signals))[:, None, :], torch.tensor(labels, dtype=torch.long)

class RhythmCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv1d(1, 12, kernel_size=7, padding=3), nn.ReLU(),
            nn.MaxPool1d(2), nn.Conv1d(12, 24, kernel_size=5, padding=2),
            nn.ReLU(), nn.AdaptiveAvgPool1d(1), nn.Flatten(), nn.Linear(24, 2)
        )
    def forward(self, x):
        return self.net(x)

def train(epochs=5):
    torch.manual_seed(42)
    x, y = synthetic()
    model = RhythmCNN()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    loss_fn = nn.CrossEntropyLoss()
    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        loss = loss_fn(model(x[:320]), y[:320])
        loss.backward()
        optimizer.step()
        model.eval()
        with torch.no_grad():
            acc = (model(x[320:]).argmax(1) == y[320:]).float().mean().item()
        print(f"epoch={epoch+1} loss={loss.item():.4f} synthetic_holdout_accuracy={acc:.3f}")
    return model

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=5)
    train(parser.parse_args().epochs)
