"""PCA + Ridge per target gene. Non-spatial strong baseline."""
from __future__ import annotations

import numpy as np
from sklearn.decomposition import PCA
from sklearn.linear_model import Ridge


def fit_pca_ridge(
    X_train: np.ndarray,
    Y_train: np.ndarray,
    n_components: int = 64,
    alpha: float = 1.0,
    random_state: int = 0,
):
    pca = PCA(n_components=n_components, random_state=random_state).fit(X_train)
    Z = pca.transform(X_train)
    models = [Ridge(alpha=alpha).fit(Z, Y_train[:, j]) for j in range(Y_train.shape[1])]
    return pca, models


def predict_pca_ridge(X_test: np.ndarray, fitted) -> np.ndarray:
    pca, models = fitted
    Z = pca.transform(X_test)
    return np.column_stack([m.predict(Z) for m in models])
