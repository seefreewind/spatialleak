"""Split 1: naive random spot-level split (80/10/10)."""
from __future__ import annotations

import numpy as np
import pandas as pd

from .base import Split


def random_spot_split(
    obs: pd.DataFrame,
    seed: int = 0,
    train_frac: float = 0.8,
    val_frac: float = 0.1,
    name: str = "random_spot",
) -> Split:
    """Random spot split WITHOUT any spatial/group constraint (naive baseline).

    Warning: this is the leakage-prone reference protocol under study.
    """
    rng = np.random.default_rng(seed)
    n = len(obs)
    perm = rng.permutation(n)
    n_train = int(round(n * train_frac))
    n_val = int(round(n * val_frac))
    train_idx = perm[:n_train].tolist()
    val_idx = perm[n_train : n_train + n_val].tolist()
    test_idx = perm[n_train + n_val :].tolist()
    split = Split(
        name=name,
        method="random_spot",
        params={"train_frac": train_frac, "val_frac": val_frac},
        seed=seed,
        train_idx=train_idx,
        val_idx=val_idx,
        test_idx=test_idx,
    )
    split.check_valid(n)
    return split
