#!/usr/bin/env python3
"""Phase 18 sample-size audit and random-size-matched control.

This script reconstructs the official random/matched-hop split geometry and
runs the limited defensive control requested in Phase 18:
datasets DLPFC, Visium breast, and GSE278936 prostate; models PCA+Ridge and
spatial kNN; hop2 and hop5 only. It does not overwrite formal benchmark outputs.
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
from dataclasses import dataclass
from pathlib import Path

import anndata as ad
import numpy as np
import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.metrics.metrics import aggregate_metrics, per_gene_metrics
from src.models.pca_ridge import fit_pca_ridge, predict_pca_ridge
from src.models.spatial_knn import predict_spatial_knn
from src.splits.base import Split
from src.splits.matched_block_split import matched_block_split
from src.splits.random_split import random_spot_split

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("sample_size_defense")


@dataclass(frozen=True)
class DatasetSpec:
    dataset: str
    label: str
    h5ad: Path
    moran_csv: Path
    aggregate_csv: Path
    seeds: tuple[int, ...]
    target_gene_csv: Path | None = None
    dlpfc_layers: bool = False


SPECS = {
    "dlpfc": DatasetSpec(
        dataset="dlpfc",
        label="DLPFC",
        h5ad=Path("data/processed/dlpfc_hvg2000.h5ad"),
        moran_csv=Path("data/processed/moran_top_genes.csv"),
        aggregate_csv=Path("results/formal_dlpfc/formal_aggregate.csv"),
        seeds=tuple(range(10)),
        dlpfc_layers=True,
    ),
    "visium_breast": DatasetSpec(
        dataset="visium_breast",
        label="Visium breast",
        h5ad=Path("data/processed/visium_breast_hvg2000.h5ad"),
        moran_csv=Path("data/processed/visium_breast_moran.csv"),
        aggregate_csv=Path("results/visium_breast_v01/v01_aggregate.csv"),
        seeds=tuple(range(10)),
    ),
    "gse278936_prostate": DatasetSpec(
        dataset="gse278936_prostate",
        label="GSE278936 prostate",
        h5ad=Path("data/processed/gse278936_prostate_hvg2000.h5ad"),
        moran_csv=Path("data/processed/gse278936_prostate_moran.csv"),
        aggregate_csv=Path("results/gse278936_prostate_spatial_pilot/spatial_pilot_aggregate.csv"),
        seeds=tuple(range(5)),
        target_gene_csv=Path("data/processed/gene_panels/shared_panel_50_gse278936_prostate_targets.csv"),
    ),
}


def _load_cfg() -> dict:
    cfg = yaml.safe_load(open("configs/experiments/formal_dlpfc.yaml"))
    cfg["hop_buffers"] = [0, 2, 5]
    cfg["models"] = ["pca_ridge", "spatial_knn"]
    return cfg


def _read_target_genes(spec: DatasetSpec, adata, cfg: dict) -> list[str]:
    if spec.target_gene_csv:
        genes = pd.read_csv(spec.target_gene_csv)["gene"].dropna().tolist()
    elif spec.dlpfc_layers:
        genes = pd.read_csv(spec.moran_csv, index_col=0).index[: cfg["n_target_genes"]].tolist()
    else:
        genes = pd.read_csv(spec.moran_csv)["gene"].dropna().head(cfg["n_target_genes"]).tolist()
    return [g for g in genes if g in adata.var_names]


def _load_design(spec: DatasetSpec, cfg: dict):
    adata = ad.read_h5ad(spec.h5ad)
    obs = adata.obs.reset_index(drop=True)
    obs["slide"] = obs["slide"].astype(str)
    if "patient" in obs.columns:
        obs["patient"] = obs["patient"].astype(str)
    if spec.dlpfc_layers:
        obs["layer"] = obs["layer"].astype(str)
        layer_dummies = pd.get_dummies(obs["layer"], prefix="layer")
        for col in layer_dummies.columns:
            obs[col] = layer_dummies[col].values
    elif "layer" in obs.columns:
        obs = obs.drop(columns=["layer"])
    if "array_row" not in obs.columns:
        obs["array_row"] = [str(n).split("-")[0].split("x")[0] for n in adata.obs_names]
        obs["array_col"] = [str(n).split("-")[0].split("x")[1] for n in adata.obs_names]
    obs["array_row"] = obs["array_row"].astype(float)
    obs["array_col"] = obs["array_col"].astype(float)

    target_genes = _read_target_genes(spec, adata, cfg)
    feature_genes = [g for g in adata.var_names if g not in target_genes][: cfg["n_features"]]
    X = np.asarray(
        adata[:, feature_genes].X.toarray()
        if hasattr(adata[:, feature_genes].X, "toarray")
        else adata[:, feature_genes].X
    )
    Y = np.asarray(
        adata[:, target_genes].X.toarray()
        if hasattr(adata[:, target_genes].X, "toarray")
        else adata[:, target_genes].X
    )
    obs["moran_signal"] = Y.mean(axis=1)
    coords = obs[["array_row", "array_col"]].values.astype(float)
    for slide in obs["slide"].unique():
        mask = (obs["slide"] == slide).values
        coords[mask] = (coords[mask] - coords[mask].mean(axis=0)) / (coords[mask].std(axis=0) + 1e-6)
    return obs, X, Y, coords, target_genes


def _build_splits(obs: pd.DataFrame, cfg: dict, seed: int) -> dict[str, Split]:
    layer_cols = [c for c in obs.columns if c.startswith("layer_")]
    splits = {"random": random_spot_split(obs, seed=seed)}
    for hop in [0, 2, 5]:
        splits[f"matched_hop{hop}"] = matched_block_split(
            obs,
            seed=seed,
            buffer_kind="hop",
            buffer_value=hop,
            n_candidates=cfg["n_candidates"],
            knn_k=cfg["knn_k"],
            layer_cols=layer_cols,
            name=f"matched_hop{hop}",
        )
    return splits


def _section_counts(obs: pd.DataFrame, idx: list[int]) -> tuple[int, int]:
    if not idx:
        return 0, 0
    sub = obs.iloc[np.asarray(idx, dtype=int)]
    patients = sub["patient"].nunique() if "patient" in sub.columns else np.nan
    return int(sub["slide"].nunique()), int(patients) if not pd.isna(patients) else -1


def _sample_size_rows(spec: DatasetSpec, obs: pd.DataFrame, target_genes: list[str], cfg: dict) -> list[dict]:
    rows = []
    for seed in spec.seeds:
        splits = _build_splits(obs, cfg, seed)
        random_split = splits["random"]
        for split_name in ["random", "matched_hop0", "matched_hop2", "matched_hop5"]:
            sp = splits[split_name]
            train_sections, train_patients = _section_counts(obs, sp.train_idx)
            val_sections, val_patients = _section_counts(obs, sp.val_idx)
            test_sections, test_patients = _section_counts(obs, sp.test_idx)
            prebuffer_test = len(sp.test_idx) + len(sp.dropped_idx)
            rows.append(
                {
                    "dataset": spec.dataset,
                    "dataset_label": spec.label,
                    "seed": seed,
                    "split": split_name,
                    "n_total": len(obs),
                    "n_train": len(sp.train_idx),
                    "n_val": len(sp.val_idx),
                    "n_test": len(sp.test_idx),
                    "n_dropped": len(sp.dropped_idx),
                    "train_fraction_vs_random": len(sp.train_idx) / len(random_split.train_idx),
                    "test_fraction_vs_random": len(sp.test_idx) / len(random_split.test_idx),
                    "test_fraction_vs_prebuffer": len(sp.test_idx) / prebuffer_test if prebuffer_test else np.nan,
                    "train_sections": train_sections,
                    "val_sections": val_sections,
                    "test_sections": test_sections,
                    "train_patients": train_patients,
                    "val_patients": val_patients,
                    "test_patients": test_patients,
                    "target_genes": len(target_genes),
                    "n_candidates": cfg["n_candidates"],
                    "knn_k": cfg["knn_k"],
                }
            )
    return rows


def _stratified_downsample(
    pool_idx: list[int],
    target_idx: list[int],
    target_total: int,
    obs: pd.DataFrame,
    rng: np.random.Generator,
) -> tuple[list[int], bool]:
    pool = np.asarray(pool_idx, dtype=int)
    if target_total >= len(pool):
        return rng.permutation(pool).tolist(), target_total == len(pool)
    target = np.asarray(target_idx, dtype=int)
    target_counts = obs.iloc[target]["slide"].value_counts()
    pool_by_slide = {s: g.index.to_numpy(dtype=int) for s, g in obs.iloc[pool].groupby("slide", sort=False)}
    proportions = target_counts / target_counts.sum()
    raw = proportions * target_total
    alloc = np.floor(raw).astype(int)
    for slide in (raw - alloc).sort_values(ascending=False).index[: target_total - int(alloc.sum())]:
        alloc.loc[slide] += 1

    chosen = []
    leftover = []
    for slide, available in pool_by_slide.items():
        rng.shuffle(available)
        want = int(alloc.get(slide, 0))
        take = min(want, len(available))
        chosen.extend(available[:take].tolist())
        leftover.extend(available[take:].tolist())
    if len(chosen) < target_total:
        rest = rng.permutation(np.asarray(leftover, dtype=int))[: target_total - len(chosen)]
        chosen.extend(rest.tolist())
    return rng.permutation(np.asarray(chosen[:target_total], dtype=int)).tolist(), len(chosen) == target_total


def _make_size_matched_random(obs: pd.DataFrame, random_sp: Split, strict_sp: Split, seed: int, hop: int) -> tuple[Split, dict]:
    rng = np.random.default_rng(10_000 + seed * 100 + hop)
    train_idx, train_exact = _stratified_downsample(
        random_sp.train_idx, strict_sp.train_idx, len(strict_sp.train_idx), obs, rng
    )
    val_idx, val_exact = _stratified_downsample(
        random_sp.val_idx, strict_sp.val_idx, len(strict_sp.val_idx), obs, rng
    )
    test_idx, test_exact = _stratified_downsample(
        random_sp.test_idx, strict_sp.test_idx, len(strict_sp.test_idx), obs, rng
    )
    sp = Split(
        name=f"random_size_matched_hop{hop}",
        method="random_spot_downsampled_to_matched_hop_size",
        params={
            "target_split": f"matched_hop{hop}",
            "composition_target": "slide_proportions",
            "train_exact": train_exact,
            "val_exact": val_exact,
            "test_exact": test_exact,
        },
        seed=seed,
        train_idx=train_idx,
        val_idx=val_idx,
        test_idx=test_idx,
        dropped_idx=[],
    )
    return sp, {
        "train_exact": train_exact,
        "val_exact": val_exact,
        "test_exact": test_exact,
        "target_n_train": len(strict_sp.train_idx),
        "target_n_val": len(strict_sp.val_idx),
        "target_n_test": len(strict_sp.test_idx),
        "actual_n_train": len(train_idx),
        "actual_n_val": len(val_idx),
        "actual_n_test": len(test_idx),
    }


def _run_model(model: str, X, Y, coords, split: Split, params: dict, seed: int):
    tr = np.asarray(split.train_idx, dtype=int)
    te = np.asarray(split.test_idx, dtype=int)
    if model == "pca_ridge":
        fit = fit_pca_ridge(
            X[tr],
            Y[tr],
            n_components=params["pca_components"],
            alpha=params["ridge_alpha"],
            random_state=seed,
        )
        return predict_pca_ridge(X[te], fit)
    if model == "spatial_knn":
        return predict_spatial_knn(coords[tr], Y[tr], coords[te], k=params["knn_k"])
    raise ValueError(model)


def _control_rows(spec: DatasetSpec, obs, X, Y, coords, target_genes, cfg):
    rows = []
    meta_rows = []
    for seed in spec.seeds:
        splits = _build_splits(obs, cfg, seed)
        for hop in [2, 5]:
            sp, meta = _make_size_matched_random(obs, splits["random"], splits[f"matched_hop{hop}"], seed, hop)
            meta_rows.append({"dataset": spec.dataset, "seed": seed, "hop": hop, **meta})
            for model in ["pca_ridge", "spatial_knn"]:
                log.info("%s seed%s hop%s %s", spec.dataset, seed, hop, model)
                pred = _run_model(model, X, Y, coords, sp, cfg["model_params"], seed)
                gm = per_gene_metrics(Y[np.asarray(sp.test_idx, dtype=int)], pred, target_genes)
                agg = aggregate_metrics(gm)
                rows.append(
                    {
                        "dataset": spec.dataset,
                        "dataset_label": spec.label,
                        "seed": seed,
                        "hop": hop,
                        "split": sp.name,
                        "model": model,
                        **agg,
                    }
                )
    return rows, meta_rows


def _load_official_for_join(spec: DatasetSpec) -> pd.DataFrame:
    df = pd.read_csv(spec.aggregate_csv)
    df = df[df["model"].isin(["pca_ridge", "spatial_knn"])].copy()
    df["dataset"] = spec.dataset
    return df


def _build_comparison(control_df: pd.DataFrame, specs: dict[str, DatasetSpec]) -> pd.DataFrame:
    official = pd.concat([_load_official_for_join(s) for s in specs.values()], ignore_index=True)
    rows = []
    for _, r in control_df.iterrows():
        dataset, seed, model, hop = r["dataset"], int(r["seed"]), r["model"], int(r["hop"])
        rand = official[
            (official.dataset == dataset)
            & (official.seed == seed)
            & (official.model == model)
            & (official.split == "random")
        ]
        strict = official[
            (official.dataset == dataset)
            & (official.seed == seed)
            & (official.model == model)
            & (official.split == f"matched_hop{hop}")
        ]
        if rand.empty or strict.empty:
            continue
        random_mean = float(rand.iloc[0]["mean_pearson"])
        random_med = float(rand.iloc[0]["median_pearson"])
        strict_mean = float(strict.iloc[0]["mean_pearson"])
        strict_med = float(strict.iloc[0]["median_pearson"])
        size_mean = float(r["mean_pearson"])
        li = random_mean - strict_mean
        rli = li / random_mean if abs(random_mean) >= 0.05 else np.nan
        rows.append(
            {
                "dataset": dataset,
                "dataset_label": SPECS[dataset].label,
                "seed": seed,
                "model": model,
                "hop": hop,
                "random_full_mean_pearson": random_mean,
                "random_size_matched_mean_pearson": size_mean,
                "spatial_buffer_mean_pearson": strict_mean,
                "random_full_median_pearson": random_med,
                "random_size_matched_median_pearson": float(r["median_pearson"]),
                "spatial_buffer_median_pearson": strict_med,
                "delta_size": random_mean - size_mean,
                "delta_spatial": size_mean - strict_mean,
                "li_random_full_vs_spatial": li,
                "rli_random_full_vs_spatial": rli,
            }
        )
    return pd.DataFrame(rows)


def _write_report(sample_df: pd.DataFrame, meta_df: pd.DataFrame, comparison_df: pd.DataFrame, out: Path):
    summary = (
        sample_df[sample_df["split"].isin(["matched_hop0", "matched_hop2", "matched_hop5"])]
        .groupby(["dataset_label", "split"])
        .agg(
            n_train=("n_train", "mean"),
            n_val=("n_val", "mean"),
            n_test=("n_test", "mean"),
            n_dropped=("n_dropped", "mean"),
            test_retained=("test_fraction_vs_prebuffer", "mean"),
            train_vs_random=("train_fraction_vs_random", "mean"),
        )
        .reset_index()
    )
    comp_summary = (
        comparison_df.groupby(["dataset_label", "model", "hop"])
        .agg(
            random_full=("random_full_mean_pearson", "mean"),
            random_size_matched=("random_size_matched_mean_pearson", "mean"),
            spatial_buffer=("spatial_buffer_mean_pearson", "mean"),
            delta_size=("delta_size", "mean"),
            delta_spatial=("delta_spatial", "mean"),
        )
        .reset_index()
    )
    exact = (
        meta_df.groupby(["dataset", "hop"])
        .agg(
            train_exact=("train_exact", "mean"),
            val_exact=("val_exact", "mean"),
            test_exact=("test_exact", "mean"),
        )
        .reset_index()
    )
    text = [
        "# Phase 18 Sample-Size Matching Audit",
        "",
        "## Decision",
        "",
        "Existing matched-hop splits do not fully control sample size. The matched-block assignment keeps the training set fixed across hop buffers within a seed, but the hop buffer removes only test spots. Random spot splits also use a different train/validation/test geometry from the matched-block splits. The project should therefore include the limited random-size-matched control requested in Phase 18.",
        "",
        "## Split-Size Summary",
        "",
        summary.to_markdown(index=False, floatfmt=".3f"),
        "",
        "## Random-Size-Matched Feasibility",
        "",
        "Exact matching means the random partition had enough train, validation, or test spots to downsample to the strict matched-hop count. Values below 1.0 identify capped comparisons where the random partition was already smaller than the strict target.",
        "",
        exact.to_markdown(index=False, floatfmt=".3f"),
        "",
        "## Defensive Control Summary",
        "",
        comp_summary.to_markdown(index=False, floatfmt=".4f"),
        "",
        "## Interpretation",
        "",
        "The defensive comparison separates two effects: performance lost by reducing the random split to a similar sample size, and performance lost after imposing spatial separation. The manuscript should emphasize the latter only when delta_spatial exceeds delta_size in the relevant dataset/model/hop comparison. GSE278936 remains a spatial-channel external replication only, because its public GEO design has one section per patient and cannot separate patient and section effects.",
        "",
        "## Provenance Notes",
        "",
        "- DLPFC formal aggregate results contain hop2/hop5 performance, but the current split JSON manifests were later overwritten by a restricted split-filter run. Split sizes in this audit were reconstructed from `configs/experiments/formal_dlpfc.yaml` and the frozen split implementation rather than read from those overwritten JSON files.",
        "- The control reuses the original random split for each seed, then downsamples train/validation/test indices without using strict-split performance.",
        "- The split-size table is written to `results/paper_assets/table_split_sample_sizes.csv`.",
        "- The control comparison table is written to `results/paper_assets/table_random_size_matched_control.csv`.",
    ]
    out.write_text("\n".join(text) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--datasets", default="dlpfc,visium_breast,gse278936_prostate")
    ap.add_argument("--skip-control", action="store_true")
    args = ap.parse_args()
    cfg = _load_cfg()
    selected = {k: SPECS[k] for k in args.datasets.split(",")}

    Path("results/paper_assets").mkdir(parents=True, exist_ok=True)
    Path("results/sample_size_control").mkdir(parents=True, exist_ok=True)
    Path("docs/reports").mkdir(parents=True, exist_ok=True)

    sample_rows = []
    control_rows = []
    meta_rows = []
    for key, spec in selected.items():
        log.info("Loading %s", key)
        obs, X, Y, coords, target_genes = _load_design(spec, cfg)
        sample_rows.extend(_sample_size_rows(spec, obs, target_genes, cfg))
        if not args.skip_control:
            rows, meta = _control_rows(spec, obs, X, Y, coords, target_genes, cfg)
            control_rows.extend(rows)
            meta_rows.extend(meta)
        del obs, X, Y, coords

    sample_df = pd.DataFrame(sample_rows)
    sample_df.to_csv("results/paper_assets/table_split_sample_sizes.csv", index=False)

    if control_rows:
        control_df = pd.DataFrame(control_rows)
        meta_df = pd.DataFrame(meta_rows)
        comparison_df = _build_comparison(control_df, selected)
        control_df.to_csv("results/sample_size_control/random_size_matched_per_seed.csv", index=False)
        meta_df.to_csv("results/sample_size_control/random_size_matched_split_meta.csv", index=False)
        comparison_df.to_csv("results/paper_assets/table_random_size_matched_control.csv", index=False)
    else:
        meta_df = pd.DataFrame()
        comparison_df = pd.DataFrame()
    _write_report(sample_df, meta_df, comparison_df, Path("docs/reports/SAMPLE_SIZE_MATCHING_AUDIT.md"))
    manifest = {
        "datasets": list(selected),
        "models": ["pca_ridge", "spatial_knn"],
        "hops": [2, 5],
        "outputs": [
            "results/paper_assets/table_split_sample_sizes.csv",
            "results/paper_assets/table_random_size_matched_control.csv",
            "results/sample_size_control/random_size_matched_per_seed.csv",
            "results/sample_size_control/random_size_matched_split_meta.csv",
            "docs/reports/SAMPLE_SIZE_MATCHING_AUDIT.md",
        ],
    }
    Path("results/sample_size_control/manifest.json").write_text(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
