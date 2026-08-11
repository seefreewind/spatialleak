#!/usr/bin/env python3
"""Formal DLPFC benchmark (Phase 7A): >=10 seeds, matched spatial blocks,
kNN-hop and normalized-coordinate buffers, all folds/seeds/slides/genes saved.

Splits per seed:
  random
  matched_hop0 / hop1 / hop2 / hop5 / hop10   (matched blocks, kNN-hop buffer)
  matched_coord0.5 / coord1.0 / coord2.0      (matched blocks, z-coord buffer)
  patient_Br5292 / Br5595 / Br8100            (seed-invariant donor folds)

Models: mean, pca_ridge, spatial_knn (GraphSAGE: run_graphsage_formal.py)

Usage: python scripts/formal_benchmark.py --config configs/experiments/formal_dlpfc.yaml
"""
import argparse
import json
import logging
import sys
import time
from pathlib import Path

import anndata as ad
import numpy as np
import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.metrics.metrics import aggregate_metrics, per_gene_metrics
from src.models.mean_model import predict_mean
from src.models.pca_ridge import fit_pca_ridge, predict_pca_ridge
from src.models.spatial_knn import predict_spatial_knn
from src.splits.group_split import group_held_out_split
from src.splits.matched_block_split import matched_block_split
from src.splits.random_split import random_spot_split
from src.splits.region_holdout_split import region_holdout_split

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("formal")


def build_splits(obs: pd.DataFrame, cfg: dict, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    obs = obs.reset_index(drop=True)
    layer_cols = [c for c in obs.columns if c.startswith("layer_")]
    splits = {"random": random_spot_split(obs, seed=seed)}
    for h in cfg["hop_buffers"]:
        splits[f"matched_hop{h}"] = matched_block_split(
            obs, seed=seed, buffer_kind="hop", buffer_value=h,
            n_candidates=cfg["n_candidates"], knn_k=cfg["knn_k"],
            layer_cols=layer_cols, name=f"matched_hop{h}")
    for t in cfg["coord_buffers"]:
        splits[f"matched_coord{t}"] = matched_block_split(
            obs, seed=seed, buffer_kind="coord", buffer_value=t,
            n_candidates=cfg["n_candidates"], layer_cols=layer_cols,
            name=f"matched_coord{t}")
    if seed == cfg["seeds"][0]:
        for donor in sorted(obs["donor"].unique()):
            test_slides = sorted(obs.loc[obs["donor"] == donor, "slide"].unique())
            train_donors = [d for d in sorted(obs["donor"].unique()) if d != donor]
            val_slides = [sorted(obs.loc[obs["donor"] == train_donors[0], "slide"].unique())[0]]
            splits[f"patient_{donor}"] = group_held_out_split(
                obs, "slide", seed=seed, test_groups=test_slides, val_groups=val_slides,
                name=f"patient_holdout_{donor}")
        # distance-curve high-hop extension (fixed geometry, seed-invariant):
        # edges-only train => test hops ~6-14; hop5 keeps ~100%, hop10 ~64%
        splits["region_hop5"] = region_holdout_split(
            obs, seed=seed, buffer_value=5, adjacent_train=False, name="region_edges_hop5")
        splits["region_hop10"] = region_holdout_split(
            obs, seed=seed, buffer_value=10, adjacent_train=False, name="region_edges_hop10")
    return splits


def run_model(model: str, X, Y, coords, split, params, seed: int) -> np.ndarray:
    tr = np.asarray(split.train_idx, dtype=int)
    te = np.asarray(split.test_idx, dtype=int)
    if len(te) == 0:
        return np.zeros((0, Y.shape[1]))
    if model == "mean":
        return predict_mean(X[tr], Y[tr], X[te])
    if model == "pca_ridge":
        fit = fit_pca_ridge(X[tr], Y[tr], n_components=params["pca_components"],
                            alpha=params["ridge_alpha"], random_state=seed)
        return predict_pca_ridge(X[te], fit)
    if model == "spatial_knn":
        return predict_spatial_knn(coords[tr], Y[tr], coords[te], k=params["knn_k"])
    raise ValueError(f"unknown model: {model}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/experiments/formal_dlpfc.yaml")
    ap.add_argument("--splits", default=None, help="comma list filter")
    ap.add_argument("--models", default=None)
    ap.add_argument("--gene-csv", default=None, help="explicit target gene list CSV")
    ap.add_argument("--out-suffix", default="")
    args = ap.parse_args()
    cfg = yaml.safe_load(open(args.config))
    if args.splits:
        cfg["splits_filter"] = args.splits.split(",")
    if args.models:
        cfg["models"] = args.models.split(",")
    out_dir = Path(cfg["out_dir"])
    (out_dir / "splits").mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    adata = ad.read_h5ad(cfg["h5ad"])
    obs = adata.obs.reset_index(drop=True)
    obs["layer"] = obs["layer"].astype(str)
    layer_dummies = pd.get_dummies(obs["layer"], prefix="layer")
    for c in layer_dummies.columns:
        obs[c] = layer_dummies[c].values
    log.info(f"Loaded {adata.n_obs} spots x {adata.n_vars} genes")

    if args.gene_csv:
        target_genes = pd.read_csv(args.gene_csv)["gene"].tolist()
    else:
        target_genes = pd.read_csv(Path(cfg["moran_csv"]), index_col=0).index[:cfg["n_target_genes"]].tolist()
    target_genes = [g for g in target_genes if g in adata.var_names]
    feature_genes = [g for g in adata.var_names if g not in target_genes][:cfg["n_features"]]
    X = np.asarray(adata[:, feature_genes].X.toarray() if hasattr(adata.X, "toarray") else adata[:, feature_genes].X)
    Y = np.asarray(adata[:, target_genes].X.toarray() if hasattr(adata.X, "toarray") else adata[:, target_genes].X)
    obs["moran_signal"] = Y.mean(axis=1)  # matching feature (documented in ANALYSIS_LOCK)
    coords = obs[["array_row", "array_col"]].values.astype(float)
    for slide in obs["slide"].unique():
        m = (obs["slide"] == slide).values
        coords[m] = (coords[m] - coords[m].mean(axis=0)) / coords[m].std(axis=0)
    del adata

    filt = set(cfg.get("splits_filter", []))
    rows, gene_rows, slide_rows = [], [], []
    for seed in cfg["seeds"]:
        splits = build_splits(obs, cfg, seed)
        meta = {}
        for sname, sp in splits.items():
            if filt and not any(sname.startswith(f) or sname == f for f in filt):
                continue
            if seed != cfg["seeds"][0] and (sname.startswith("patient_")
                                            or sname.startswith("region_")):
                continue  # seed-invariant splits: run once
            meta[sname] = {
                "n_train": len(sp.train_idx), "n_val": len(sp.val_idx),
                "n_test": len(sp.test_idx), "n_dropped": len(sp.dropped_idx),
                "params": sp.params,
            }
            for model in cfg["models"]:
                t = time.time()
                test_pos = np.asarray(sp.test_idx, dtype=int)
                pred = run_model(model, X, Y, coords, sp, cfg["model_params"], seed)
                if len(test_pos) == 0:
                    log.warning(f"  seed{seed} {sname} {model}: EMPTY test set, skipped")
                    continue
                gm = per_gene_metrics(Y[test_pos], pred, target_genes)
                agg = aggregate_metrics(gm)
                gm.insert(0, "split", sname); gm.insert(1, "model", model); gm.insert(2, "seed", seed)
                gene_rows.append(gm)
                rows.append({"split": sname, "model": model, "seed": seed, **agg})
                for slide, idx in obs.iloc[test_pos].groupby("slide").indices.items():
                    sm = per_gene_metrics(Y[test_pos[idx]], pred[idx], target_genes)
                    sm.insert(0, "slide", slide); sm.insert(1, "split", sname)
                    sm.insert(2, "model", model); sm.insert(3, "seed", seed)
                    slide_rows.append(sm)
                log.info(f"  seed{seed} {sname} {model}: {agg['mean_pearson']:.4f} ({time.time()-t:.0f}s)")
        (out_dir / "splits" / f"seed{seed}.json").write_text(json.dumps(meta, indent=2))

    suffix = f"_{args.out_suffix}" if args.out_suffix else ""
    pd.concat(gene_rows, ignore_index=True).to_csv(out_dir / f"formal_per_gene{suffix}.csv", index=False)
    pd.concat(slide_rows, ignore_index=True).to_csv(out_dir / f"formal_per_gene_per_slide{suffix}.csv", index=False)
    pd.DataFrame(rows).to_csv(out_dir / f"formal_aggregate{suffix}.csv", index=False)
    (out_dir / "formal_config.yaml").write_text(yaml.safe_dump(cfg))
    log.info(f"\nDone in {time.time()-t0:.0f}s -> {out_dir}")


if __name__ == "__main__":
    main()
