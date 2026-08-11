#!/usr/bin/env python3
"""External dataset benchmark: random, matched spatial buffers, region hop
curves, patient-held-out folds, and slide-held-out folds.

The defaults preserve the Phase 7A V0.1 behavior. Formal external runs should
set --seeds 0,1,2,3,4,5,6,7,8,9 and an explicit --out-dir to avoid overwriting
V0.1 outputs.

Usage: python scripts/benchmark_external.py --dataset anderson --config configs/experiments/formal_dlpfc.yaml
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
log = logging.getLogger("external")


def _parse_csv_values(text, cast=str) -> list:
    if text is None:
        return []
    return [cast(x) for x in text.split(",") if str(x).strip() != ""]


def _split_meta(split) -> dict:
    return {
        "n_train": len(split.train_idx),
        "n_val": len(split.val_idx),
        "n_test": len(split.test_idx),
        "n_dropped": len(split.dropped_idx),
        "params": split.params,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True,
                    choices=["anderson", "thrane", "visium_breast", "gse278936_prostate"])
    ap.add_argument("--config", default="configs/experiments/formal_dlpfc.yaml")
    ap.add_argument("--seeds", default="0,1,2,3,4")
    ap.add_argument("--gene-csv", default=None, help="explicit target gene list CSV (gene column)")
    ap.add_argument("--splits", default=None, help="comma list: random,matched_hop0,patient")
    ap.add_argument("--out-dir", default=None, help="default: results/{dataset}_v01")
    ap.add_argument("--out-prefix", default="v01")
    ap.add_argument("--hop-buffers", default="0", help="matched hop buffers, e.g. 0,1,2,5")
    ap.add_argument("--coord-buffers", default="", help="matched normalized-coordinate buffers")
    ap.add_argument("--region-hops", default="", help="region holdout high-hop buffers")
    ap.add_argument("--patient-each-seed", action="store_true",
                    help="run deterministic patient folds for every seed instead of once")
    ap.add_argument("--slide-holdout", action="store_true",
                    help="run deterministic slide-held-out folds once")
    args = ap.parse_args()
    cfg = yaml.safe_load(open(args.config))
    proc = Path(cfg.get("processed_dir", Path(cfg["h5ad"]).parent))
    out_dir = Path(args.out_dir) if args.out_dir else Path("results") / f"{args.dataset}_v01"
    (out_dir / "splits").mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    seeds = _parse_csv_values(args.seeds, int)
    split_filters = set(_parse_csv_values(args.splits)) if args.splits else set()
    hop_buffers = _parse_csv_values(args.hop_buffers, int)
    coord_buffers = _parse_csv_values(args.coord_buffers, float)
    region_hops = _parse_csv_values(args.region_hops, int)

    h5ad_path = proc / f"{args.dataset}_hvg2000.h5ad"
    moran_path = proc / f"{args.dataset}_moran.csv"

    adata = ad.read_h5ad(h5ad_path)
    obs = adata.obs.reset_index(drop=True)
    obs["patient"] = obs["patient"].astype(str)
    obs["slide"] = obs["slide"].astype(str)
    if "layer" in obs.columns:
        obs = obs.drop(columns=["layer"])
    layer_cols = []
    moran = pd.read_csv(moran_path)
    if args.gene_csv:
        target_genes = pd.read_csv(args.gene_csv)["gene"].tolist()
    else:
        target_genes = moran["gene"].dropna().head(cfg["n_target_genes"]).tolist()
    target_genes = [g for g in target_genes if g in adata.var_names]
    feature_genes = [g for g in adata.var_names if g not in target_genes][:cfg["n_features"]]
    X = np.asarray(adata[:, feature_genes].X.toarray() if hasattr(adata.X, "toarray") else adata[:, feature_genes].X)
    Y = np.asarray(adata[:, target_genes].X.toarray() if hasattr(adata.X, "toarray") else adata[:, target_genes].X)
    if "array_row" not in obs.columns:
        obs["array_row"] = [str(n).split("-")[0].split("x")[0] for n in adata.obs_names]
        obs["array_col"] = [str(n).split("-")[0].split("x")[1] for n in adata.obs_names]
    obs["array_row"] = obs["array_row"].astype(float)
    obs["array_col"] = obs["array_col"].astype(float)
    obs["moran_signal"] = Y.mean(axis=1)
    coords = obs[["array_row", "array_col"]].values.astype(float)
    for slide in obs["slide"].unique():
        m = (obs["slide"] == slide).values
        coords[m] = (coords[m] - coords[m].mean(axis=0)) / coords[m].std(axis=0)
    log.info(f"{args.dataset}: {adata.n_obs} spots x {adata.n_vars} genes, "
             f"{obs['patient'].nunique()} patients, {obs['slide'].nunique()} sections")

    rows, gene_rows, slide_rows = [], [], []
    for seed in seeds:
        splits = {"random": random_spot_split(obs, seed=seed)}
        for h in hop_buffers:
            splits[f"matched_hop{h}"] = matched_block_split(
                obs, seed=seed, buffer_kind="hop", buffer_value=h,
                n_candidates=cfg["n_candidates"], knn_k=cfg["knn_k"],
                layer_cols=layer_cols, name=f"matched_hop{h}")
        for c in coord_buffers:
            splits[f"matched_coord{c}"] = matched_block_split(
                obs, seed=seed, buffer_kind="coord", buffer_value=c,
                n_candidates=cfg["n_candidates"], knn_k=cfg["knn_k"],
                layer_cols=layer_cols, name=f"matched_coord{c}")
        if seed == seeds[0] or args.patient_each_seed:
            patients = sorted(obs["patient"].unique())
            if len(patients) > 1:
                for pat in patients:
                    test_slides = sorted(obs.loc[obs["patient"] == pat, "slide"].unique())
                    train_pats = [p for p in patients if p != pat]
                    val_slides = [sorted(obs.loc[obs["patient"] == train_pats[0], "slide"].unique())[0]]
                    splits[f"patient_{pat}"] = group_held_out_split(
                        obs, "slide", seed=seed, test_groups=test_slides, val_groups=val_slides,
                        name=f"patient_holdout_{pat}")
        if seed == seeds[0] and args.slide_holdout:
            slides = sorted(obs["slide"].unique())
            for slide in slides:
                val_candidates = [s for s in slides if s != slide]
                val_slides = [val_candidates[0]] if len(val_candidates) > 1 else []
                splits[f"slide_{slide}"] = group_held_out_split(
                    obs, "slide", seed=seed, test_groups=[slide], val_groups=val_slides,
                    name=f"slide_holdout_{slide}")
        if seed == seeds[0]:
            for h in region_hops:
                splits[f"region_hop{h}"] = region_holdout_split(
                    obs, seed=seed, buffer_value=h, knn_k=cfg["knn_k"],
                    adjacent_train=False, name=f"region_edges_hop{h}")
        meta = {}
        for sname, sp in splits.items():
            if split_filters and not any(sname.startswith(f) or sname == f for f in split_filters):
                continue
            if seed != seeds[0] and sname.startswith("patient_") and not args.patient_each_seed:
                continue
            meta[sname] = _split_meta(sp)
            for model in cfg["models"]:
                t = time.time()
                te_pos = np.asarray(sp.test_idx, dtype=int)
                if len(te_pos) == 0:
                    continue
                tr = np.asarray(sp.train_idx, dtype=int)
                if model == "mean":
                    pred = predict_mean(X[tr], Y[tr], X[te_pos])
                elif model == "pca_ridge":
                    fit = fit_pca_ridge(X[tr], Y[tr],
                                        n_components=cfg["model_params"]["pca_components"],
                                        alpha=cfg["model_params"]["ridge_alpha"], random_state=seed)
                    pred = predict_pca_ridge(X[te_pos], fit)
                elif model == "spatial_knn":
                    pred = predict_spatial_knn(coords[tr], Y[tr], coords[te_pos],
                                               k=cfg["model_params"]["knn_k"])
                gm = per_gene_metrics(Y[te_pos], pred, target_genes)
                agg = aggregate_metrics(gm)
                gm.insert(0, "split", sname); gm.insert(1, "model", model); gm.insert(2, "seed", seed)
                gene_rows.append(gm)
                rows.append({"split": sname, "model": model, "seed": seed, **agg})
                for slide, idx in obs.iloc[te_pos].groupby("slide").indices.items():
                    sm = per_gene_metrics(Y[te_pos[idx]], pred[idx], target_genes)
                    sm.insert(0, "slide", slide); sm.insert(1, "split", sname)
                    sm.insert(2, "model", model); sm.insert(3, "seed", seed)
                    slide_rows.append(sm)
                log.info(f"  seed{seed} {sname} {model}: {agg['mean_pearson']:.4f} ({time.time()-t:.0f}s)")
        (out_dir / "splits" / f"seed{seed}.json").write_text(json.dumps(meta, indent=2))

    pd.concat(gene_rows, ignore_index=True).to_csv(out_dir / f"{args.out_prefix}_per_gene.csv", index=False)
    pd.concat(slide_rows, ignore_index=True).to_csv(out_dir / f"{args.out_prefix}_per_gene_per_slide.csv", index=False)
    pd.DataFrame(rows).to_csv(out_dir / f"{args.out_prefix}_aggregate.csv", index=False)
    run_cfg = {
        **cfg,
        "dataset": args.dataset,
        "processed_dir": str(proc),
        "h5ad": str(h5ad_path),
        "moran_csv": str(moran_path),
        "out_dir": str(out_dir),
        "out_prefix": args.out_prefix,
        "seeds": seeds,
        "hop_buffers": hop_buffers,
        "coord_buffers": coord_buffers,
        "region_hops": region_hops,
        "gene_csv": args.gene_csv,
        "splits_filter": sorted(split_filters),
        "patient_each_seed": args.patient_each_seed,
        "slide_holdout": args.slide_holdout,
    }
    (out_dir / f"{args.out_prefix}_config.yaml").write_text(yaml.safe_dump(run_cfg))
    log.info(f"Done in {time.time()-t0:.0f}s -> {out_dir}")


if __name__ == "__main__":
    main()
