#!/usr/bin/env python3
"""Build the Phase 16 two-channel leakage summary table."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


OUT = Path("results/paper_assets/table_two_channel_leakage.csv")
RLI_DENOMINATOR_FLOOR = 0.05

DATASET_META = {
    "dlpfc": {
        "dataset": "DLPFC",
        "platform": "Visium_DLPFC",
        "patient_count": 3,
        "section_count": 12,
        "moran_path": "data/processed/moran_top_genes.csv",
    },
    "anderson": {
        "dataset": "Andersson",
        "platform": "ST_v1",
        "patient_count": 8,
        "section_count": 36,
        "moran_path": "data/processed/anderson_moran.csv",
    },
    "thrane": {
        "dataset": "Thrane",
        "platform": "ST_v1",
        "patient_count": 4,
        "section_count": 8,
        "moran_path": "data/processed/thrane_moran.csv",
    },
    "visium_breast": {
        "dataset": "Visium breast",
        "platform": "Visium_breast",
        "patient_count": 1,
        "section_count": 2,
        "moran_path": "data/processed/visium_breast_moran.csv",
    },
}

GRAPH_META = {
    "DLPFC": DATASET_META["dlpfc"],
    "Andersson": DATASET_META["anderson"],
    "Thrane": DATASET_META["thrane"],
    "Visium breast": DATASET_META["visium_breast"],
}


def stable_ratio(random_perf: float, strict_perf: float) -> tuple[float, float]:
    """Return RLI and retention, or NA if the random denominator is unstable."""
    if pd.isna(random_perf) or pd.isna(strict_perf) or abs(random_perf) < RLI_DENOMINATOR_FLOOR:
        return np.nan, np.nan
    return (random_perf - strict_perf) / random_perf, strict_perf / random_perf


def mean_moran(path: str, top_n: int = 50) -> float:
    df = pd.read_csv(path)
    return float(df["moran_i"].head(top_n).mean())


def add_context(row: dict, meta: dict) -> dict:
    row["MoranI"] = mean_moran(meta["moran_path"])
    row["patient_count"] = meta["patient_count"]
    row["section_count"] = meta["section_count"]
    return row


def build_dataset_specific_rows() -> list[dict]:
    df = pd.read_csv("results/final_stats/LI_RLI_all_datasets.csv")
    df = df[df["model"].ne("mean")].copy()
    rows = []
    for dataset_key, meta in DATASET_META.items():
        subset = df[df["dataset"].eq(dataset_key)]
        for model in sorted(subset["model"].unique()):
            model_df = subset[subset["model"].eq(model)]
            spatial = model_df[model_df["strict_type"].eq("spatial")]
            patient = model_df[model_df["strict_type"].eq("patient")]

            random_perf = np.nan
            spatial_strict = np.nan
            patient_strict = np.nan
            if not spatial.empty:
                random_perf = float(spatial["random"].iloc[0])
                spatial_strict = float(spatial["strict"].iloc[0])
            if not patient.empty:
                random_perf = float(patient["random"].iloc[0]) if pd.isna(random_perf) else random_perf
                patient_strict = float(patient["strict"].iloc[0])

            rli_spatial, retention_spatial = stable_ratio(random_perf, spatial_strict)
            rli_patient, retention_patient = stable_ratio(random_perf, patient_strict)
            rows.append(add_context({
                "dataset": meta["dataset"],
                "platform": meta["platform"],
                "model": model,
                "random_perf": random_perf,
                "spatial_strict_perf": spatial_strict,
                "patient_strict_perf": patient_strict,
                "RLI_spatial": rli_spatial,
                "RLI_patient": rli_patient,
                "Retention_spatial": retention_spatial,
                "Retention_patient": retention_patient,
            }, meta))
    return rows


def build_graphsage_rows() -> list[dict]:
    df = pd.read_csv("results/paper_assets/table_graphsage_shared_panel50_RLI.csv")
    rows = []
    for dataset, meta in GRAPH_META.items():
        subset = df[df["dataset"].eq(dataset)]
        spatial = subset[subset["strict_label"].str.startswith("matched_hop")]
        patient = subset[subset["strict_label"].eq("patient")]

        random_perf = np.nan
        spatial_strict = np.nan
        patient_strict = np.nan
        if not spatial.empty:
            random_perf = float(spatial["random"].iloc[0])
            spatial_strict = float(spatial["strict"].iloc[0])
        if not patient.empty:
            random_perf = float(patient["random"].iloc[0]) if pd.isna(random_perf) else random_perf
            patient_strict = float(patient["strict"].iloc[0])

        rli_spatial, retention_spatial = stable_ratio(random_perf, spatial_strict)
        rli_patient, retention_patient = stable_ratio(random_perf, patient_strict)
        rows.append(add_context({
            "dataset": meta["dataset"],
            "platform": meta["platform"],
            "model": "graphsage",
            "random_perf": random_perf,
            "spatial_strict_perf": spatial_strict,
            "patient_strict_perf": patient_strict,
            "RLI_spatial": rli_spatial,
            "RLI_patient": rli_patient,
            "Retention_spatial": retention_spatial,
            "Retention_patient": retention_patient,
        }, meta))
    return rows


def main() -> None:
    rows = build_dataset_specific_rows() + build_graphsage_rows()
    out = pd.DataFrame(rows)
    out = out[
        [
            "dataset",
            "platform",
            "model",
            "random_perf",
            "spatial_strict_perf",
            "patient_strict_perf",
            "RLI_spatial",
            "RLI_patient",
            "Retention_spatial",
            "Retention_patient",
            "MoranI",
            "patient_count",
            "section_count",
        ]
    ].sort_values(["dataset", "model"]).reset_index(drop=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT, index=False)
    print(f"wrote {OUT} ({len(out)} rows)")


if __name__ == "__main__":
    main()
