"""Lightweight transductive GraphSAGE (CPU-only) as the representative
spatial-aware complex model for the pilot.

Graph: within-slide kNN (k=10) on array coordinates. Features: PCA-64 of the
expression features (same input as PCA+Ridge for fairness). Two SAGE layers
(mean aggregation), ReLU, MSE on train nodes, early stopping on val nodes.

NOTE (leakage framing): at inference, test nodes aggregate features of their
spatial neighbors (legitimate input modality); under random splits those
neighbors are mostly train spots - exactly the information-sharing channel
this benchmark probes. Labels are never aggregated.
"""
from __future__ import annotations

import numpy as np
import torch
import torch.nn.functional as F
from scipy.spatial import cKDTree


def build_spatial_graph(coords: np.ndarray, slide_of: np.ndarray, k: int = 10) -> tuple:
    """Return edge_index (2, E) within slides (no cross-slide edges), with self-loops."""
    src, dst = [], []
    for slide in np.unique(slide_of):
        m = np.where(slide_of == slide)[0]
        tree = cKDTree(coords[m])
        d, idx = tree.query(coords[m], k=min(k + 1, len(m)))
        for i in range(len(m)):
            src.append(m[i])
            dst.append(m[i])  # self-loop
            for j in idx[i][1:]:
                src.append(m[i])
                dst.append(m[j])
    return torch.tensor([src, dst], dtype=torch.long)


class SAGEConv(torch.nn.Module):
    def __init__(self, in_dim: int, out_dim: int):
        super().__init__()
        self.lin = torch.nn.Linear(in_dim * 2, out_dim)

    def forward(self, x, edge_index):
        n = x.shape[0]
        agg = torch.zeros_like(x)
        src, dst = edge_index
        agg.index_add_(0, dst, x[src])
        counts = torch.bincount(dst, minlength=n).clamp(min=1).unsqueeze(1)
        agg = agg / counts.float()
        return F.relu(self.lin(torch.cat([x, agg], dim=1)))


class GraphSAGE(torch.nn.Module):
    def __init__(self, in_dim: int, hidden: int, out_dim: int):
        super().__init__()
        self.l1 = SAGEConv(in_dim, hidden)
        self.l2 = SAGEConv(hidden, out_dim)

    def forward(self, x, edge_index):
        return self.l2(self.l1(x, edge_index), edge_index)


def fit_graphsage(
    X_train: np.ndarray,
    Y_train: np.ndarray,
    X_all: np.ndarray,
    Y_all: np.ndarray,
    coords_all: np.ndarray,
    slide_of: np.ndarray,
    train_idx: np.ndarray,
    val_idx: np.ndarray,
    n_components: int = 64,
    hidden: int = 64,
    k: int = 10,
    epochs: int = 300,
    patience: int = 30,
    lr: float = 1e-2,
    weight_decay: float = 1e-4,
    seed: int = 0,
    device: str = "cpu",
) -> tuple:
    torch.manual_seed(seed)
    from sklearn.decomposition import PCA

    pca = PCA(n_components=n_components, random_state=seed).fit(X_train)
    Xp_np = pca.transform(X_all)
    train_mean = Xp_np[train_idx].mean(axis=0, keepdims=True)
    train_std = Xp_np[train_idx].std(axis=0, keepdims=True) + 1e-6
    Xp = torch.tensor((Xp_np - train_mean) / train_std, dtype=torch.float32, device=device)
    n_all = X_all.shape[0]
    Y_full = torch.zeros((n_all, Y_train.shape[1]), dtype=torch.float32, device=device)
    Y_full[train_idx] = torch.tensor(Y_train, dtype=torch.float32, device=device)
    Y_full[val_idx] = torch.tensor(Y_all[val_idx], dtype=torch.float32, device=device)
    tr_mask = torch.zeros(n_all, dtype=torch.bool)
    va_mask = torch.zeros(n_all, dtype=torch.bool)
    tr_mask[train_idx] = True
    va_mask[val_idx] = True

    edge_index = build_spatial_graph(coords_all, slide_of, k=k).to(device)
    model = GraphSAGE(n_components, hidden, Y_train.shape[1]).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay)

    best_loss, best_state, bad = float("inf"), None, 0
    for epoch in range(epochs):
        model.train()
        opt.zero_grad()
        out = model(Xp, edge_index)
        loss = F.mse_loss(out[tr_mask], Y_full[tr_mask])
        loss.backward()
        opt.step()
        model.eval()
        with torch.no_grad():
            vloss = F.mse_loss(model(Xp, edge_index)[va_mask], Y_full[va_mask]).item()
        if vloss < best_loss:
            best_loss, bad = vloss, 0
            best_state = {k: v.detach().clone() for k, v in model.state_dict().items()}
        else:
            bad += 1
            if bad >= patience:
                break
    model.load_state_dict(best_state)
    model.eval()
    with torch.no_grad():
        pred = model(Xp, edge_index).numpy()
    return pca, model, pred
