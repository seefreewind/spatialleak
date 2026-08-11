"""Mean predictor: per-target-gene train mean. Strong simple baseline."""
from __future__ import annotations

import numpy as np


def predict_mean(X_train: np.ndarray, Y_train: np.ndarray, X_test: np.ndarray) -> np.ndarray:
    """X: (n, n_features); Y: (n, n_targets) normalized expression."""
    del X_train
    return np.tile(Y_train.mean(axis=0), (X_test.shape[0], 1))
