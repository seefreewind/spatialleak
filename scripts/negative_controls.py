#!/usr/bin/env python3
"""Phase 13 negative controls (CPU-light, spatial kNN only):

C1  permute coordinates within slide -> kNN on scrambled coords (noise)
C2  shuffle spatial neighbor graph (equivalent: same as C1 for kNN)
C3  expression-matched random neighbors (kNN on scrambled coords, same train set)
C4  layer-stratified random spot split vs naive random split
C5  buffer sweep (distance-matched separation) -> see pilot_benchmark --splits

Expected: C1/C2/C3 collapse kNN to ~Mean level under random split;
C4 should show most (but not all) of the naive inflation persists under
stratified random split, isolating spatial-autocorrelation leakage from
compositional imbalance.

Usage: python scripts/negative_controls.py --config configs/experiments/pilot_dlpfc.yaml
"""
import argparse
import sys
import time
from pathlib import Path

import anndata as ad
import numpy as np
import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.metrics.metrics import aggregate_metrics, per_gene_metrics
from src.models.spatial_knn import predict_spatial_knn
from src.splits.random_split import random_spot_split
from src.splits.stratified_split import stratified_spot_split


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/experiments/pilot_dlpfc.yaml")
    ap.add_argument("--n_seeds", type=int, default=5)
    args = ap.parse_args()
    cfg = yaml.safe_load(open(args.config))
    out_dir = Path(cfg["out_dir"]).parent / "sensitivity"
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    adata = ad.read_h5ad(cfg["h5ad"])
    obs = adata.obs.reset_index(drop=True)
    # layer annotations from raw layer map (not in h5ad yet - join from obs if present)
    if "layer" not in obs.columns:
        layer_map = pd.read_csv("data/raw/dlpfc/barcode_level_layer_map.tsv", sep="\t")
        barcodes = [b.rsplit("-", 1)[0] for b in obs.index]
        tmp = obs.copy()
        tmp["bc"] = barcodes
        tmp = tmp.merge(layer_map.rename(columns={"barcode": "bc", "layer": "layer"}), on="bc", how="left")
        obs["layer"] = tmp["layer"].values
    obs["layer"] = obs["layer"].fillna("NA")

    target_genes = pd.read_csv(Path(cfg["moran_csv"]), index_col=0).index[:cfg["n_target_genes"]].tolist()
    target_genes = [g for g in target_genes if g in adata.var_names]
    feature_genes = [g for g in adata.var_names if g not in target_genes][:cfg["n_features"]]
    X = np.asarray(adata[:, feature_genes].X.toarray() if hasattr(adata.X, "toarray") else adata[:, feature_genes].X)
    Y = np.asarray(adata[:, target_genes].X.toarray() if hasattr(adata.X, "toarray") else adata[:, target_genes].X)
    coords = obs[["array_row", "array_col"]].values.astype(float)
    for slide in obs["slide"].unique():
        m = (obs["slide"] == slide).values
        coords[m] = (coords[m] - coords[m].mean(axis=0)) / coords[m].std(axis=0)
    del adata

    rows = []
    for seed in range(args.n_seeds):
        # naive random split (reference)
        sp = random_spot_split(obs, seed=seed)
        tr, te = np.asarray(sp.train_idx), np.asarray(sp.test_idx)
        pred = predict_spatial_knn(coords[tr], Y[tr], coords[te], k=cfg["model_params"]["knn_k"])
        rows.append({"control": "naive_random", "seed": seed,
                     **aggregate_metrics(per_gene_metrics(Y[te], pred, target_genes))})

        # C1: permute coordinates within each slide (breaks spatial signal)
        perm = np.empty_like(coords)
        for slide in obs["slide"].unique():
            m = (obs["slide"] == slide).values
            perm[m] = coords[m][np.random.default_rng(seed).permutation(m.sum())]
        pred = predict_spatial_knn(perm[tr], Y[tr], perm[te], k=cfg["model_params"]["knn_k"])
        rows.append({"control": "permuted_coords", "seed": seed,
                     **aggregate_metrics(per_gene_metrics(Y[te], pred, target_genes))})

        # C2: shuffle graph = C1 for kNN (same operation, different label)
        pred = predict_spatial_knn(coords[tr][np.random.default_rng(seed).permutation(len(tr))],
                                   Y[tr], coords[te], k=cfg["model_params"]["knn_k"])
        rows.append({"control": "shuffled_graph", "seed": seed,
                     **aggregate_metrics(per_gene_metrics(Y[te], pred, target_genes))})

        # C4: layer-stratified random split
        sps = stratified_spot_split(obs, "layer", seed=seed)
        trs, tes = np.asarray(sps.train_idx), np.asarray(sps.test_idx)
        pred = predict_spatial_knn(coords[trs], Y[trs], coords[tes], k=cfg["model_params"]["knn_k"])
        rows.append({"control": "layer_stratified_random", "seed": seed,
                     **aggregate_metrics(per_gene_metrics(Y[tes], pred, target_genes))})
        print(f"  seed {seed}: naive={rows[-4]['mean_pearson']:.3f} "
              f"perm={rows[-3]['mean_pearson']:.3f} shuffle={rows[-2]['mean_pearson']:.3f} "
              f"strat={rows[-1]['mean_pearson']:.3f}")

    df = pd.DataFrame(rows)
    df.to_csv(out_dir / "negative_controls_knn.csv", index=False)
    print("\n== Negative controls (spatial kNN, mean across seeds) ==")
    print(df.groupby("control")["mean_pearson"].agg(["mean", "std"]).round(3))
    print(f"\nDone in {time.time()-t0:.0f}s -> {out_dir / 'negative_controls_knn.csv'}")


if __name__ == "__main__":
    main()
