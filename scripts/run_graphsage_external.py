#!/usr/bin/env python3
"""GraphSAGE runs for external datasets with resume-safe CSV checkpoints."""
import argparse
import sys
import time
from pathlib import Path

import anndata as ad
import numpy as np
import pandas as pd
import torch
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.metrics.metrics import aggregate_metrics, per_gene_metrics
from src.models.graphsage import fit_graphsage
from src.splits.group_split import group_held_out_split
from src.splits.matched_block_split import matched_block_split
from src.splits.random_split import random_spot_split


def parse_seeds(text: str) -> list:
    return [int(s) for s in text.split(",") if s.strip()]


def flush(rows_prev, rows, gene_prev, gene_rows, agg_path, gene_path):
    parts = ([gene_prev] if gene_prev is not None else []) + gene_rows
    if parts:
        gene_df = pd.concat(parts, ignore_index=True)
        gene_df = gene_df.drop_duplicates(subset=["split", "model", "seed", "gene"])
        gene_df.to_csv(gene_path, index=False)
    agg_df = pd.DataFrame(rows_prev + rows)
    if len(agg_df):
        agg_df = agg_df.drop_duplicates(subset=["split", "model", "seed"])
        agg_df.to_csv(agg_path, index=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True, choices=["anderson", "thrane", "visium_breast"])
    ap.add_argument("--config", default="configs/experiments/formal_dlpfc.yaml")
    ap.add_argument("--seeds", default="0,1,2,3,4")
    ap.add_argument("--gene-csv", default=None)
    ap.add_argument("--splits", default="random,matched_hop0,patient")
    ap.add_argument("--matched-hop-values", default="0",
                    help="comma list of hop buffers to build, e.g. 0,5")
    ap.add_argument("--slide-holdout", action="store_true")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--out-prefix", default="graphsage")
    args = ap.parse_args()

    cfg = yaml.safe_load(open(args.config))
    proc = Path(cfg.get("processed_dir", Path(cfg["h5ad"]).parent))
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    agg_path = out_dir / f"{args.out_prefix}_aggregate.csv"
    gene_path = out_dir / f"{args.out_prefix}_per_gene.csv"
    rows_prev = pd.read_csv(agg_path).to_dict("records") if agg_path.exists() else []
    gene_prev = pd.read_csv(gene_path) if gene_path.exists() else None
    done = {(r["split"], r["seed"]) for r in rows_prev}
    filters = set(args.splits.split(",")) if args.splits else set()
    matched_hops = [int(v) for v in args.matched_hop_values.split(",") if v.strip()]
    torch.set_num_threads(2)
    t0 = time.time()

    adata = ad.read_h5ad(proc / f"{args.dataset}_hvg2000.h5ad")
    obs = adata.obs.reset_index(drop=True)
    obs["patient"] = obs["patient"].astype(str)
    obs["slide"] = obs["slide"].astype(str)
    moran = pd.read_csv(proc / f"{args.dataset}_moran.csv")
    if args.gene_csv:
        target_genes = pd.read_csv(args.gene_csv)["gene"].tolist()
    else:
        target_genes = moran["gene"].dropna().head(cfg["n_target_genes"]).tolist()
    target_genes = [g for g in target_genes if g in adata.var_names]
    feature_genes = [g for g in adata.var_names if g not in target_genes][:cfg["n_features"]]
    X_all = np.asarray(adata[:, feature_genes].X.toarray() if hasattr(adata.X, "toarray") else adata[:, feature_genes].X)
    Y_all = np.asarray(adata[:, target_genes].X.toarray() if hasattr(adata.X, "toarray") else adata[:, target_genes].X)
    obs["array_row"] = obs["array_row"].astype(float)
    obs["array_col"] = obs["array_col"].astype(float)
    obs["moran_signal"] = Y_all.mean(axis=1)
    coords = obs[["array_row", "array_col"]].values.astype(float)
    for slide in obs["slide"].unique():
        m = (obs["slide"] == slide).values
        coords[m] = (coords[m] - coords[m].mean(axis=0)) / coords[m].std(axis=0)
    slide_of = obs["slide"].values
    del adata

    rows, gene_rows = [], []
    seeds = parse_seeds(args.seeds)
    for seed in seeds:
        splits = {
            "random": random_spot_split(obs, seed=seed),
        }
        for hop in matched_hops:
            splits[f"matched_hop{hop}"] = matched_block_split(
                obs, seed=seed, buffer_kind="hop", buffer_value=hop,
                n_candidates=cfg["n_candidates"], knn_k=cfg["knn_k"], layer_cols=[],
                name=f"matched_hop{hop}")
        if seed == seeds[0]:
            patients = sorted(obs["patient"].unique())
            if len(patients) > 1:
                for pat in patients:
                    test_slides = sorted(obs.loc[obs["patient"] == pat, "slide"].unique())
                    train_pats = [p for p in patients if p != pat]
                    val_slides = [sorted(obs.loc[obs["patient"] == train_pats[0], "slide"].unique())[0]]
                    splits[f"patient_{pat}"] = group_held_out_split(
                        obs, "slide", seed=seed, test_groups=test_slides, val_groups=val_slides,
                        name=f"patient_holdout_{pat}")
            if args.slide_holdout:
                slides = sorted(obs["slide"].unique())
                for slide in slides:
                    val_candidates = [s for s in slides if s != slide]
                    val_slides = [val_candidates[0]] if len(val_candidates) > 1 else []
                    splits[f"slide_{slide}"] = group_held_out_split(
                        obs, "slide", seed=seed, test_groups=[slide], val_groups=val_slides,
                        name=f"slide_holdout_{slide}")

        for sname, sp in splits.items():
            if filters and not any(sname.startswith(f) or sname == f for f in filters):
                continue
            if (sname, seed) in done:
                print(f"  skip {sname} seed{seed} (already done)", flush=True)
                continue
            tr, va = np.asarray(sp.train_idx, dtype=int), np.asarray(sp.val_idx, dtype=int)
            te = np.asarray(sp.test_idx, dtype=int)
            t = time.time()
            _, _, pred = fit_graphsage(
                X_train=X_all[tr], Y_train=Y_all[tr], X_all=X_all, Y_all=Y_all,
                coords_all=coords, slide_of=slide_of, train_idx=tr, val_idx=va,
                n_components=cfg["model_params"]["pca_components"],
                hidden=128, lr=1e-3, epochs=500, patience=60,
                seed=seed, device="cpu")
            gm = per_gene_metrics(Y_all[te], pred[te], target_genes)
            gm.insert(0, "split", sname)
            gm.insert(1, "model", "graphsage")
            gm.insert(2, "seed", seed)
            gene_rows.append(gm)
            rows.append({"split": sname, "model": "graphsage", "seed": seed,
                         **aggregate_metrics(gm)})
            print(f"  {sname} seed{seed}: {rows[-1]['mean_pearson']:.4f} ({time.time()-t:.0f}s)", flush=True)
            flush(rows_prev, rows, gene_prev, gene_rows, agg_path, gene_path)

    flush(rows_prev, rows, gene_prev, gene_rows, agg_path, gene_path)
    print(f"\nDone in {time.time()-t0:.0f}s -> {out_dir}")


if __name__ == "__main__":
    main()
