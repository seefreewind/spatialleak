#!/usr/bin/env python3
"""Build Phase 19 paper tables that use train-only GraphSAGE preprocessing.

The Phase 19 audit found that the old GraphSAGE feature standardization used
the full graph after train-only PCA. Corrected external GraphSAGE reruns are
kept in *_trainonly directories. DLPFC corrected GraphSAGE was intentionally
not promoted because the full 10-seed rerun was not completed in Phase 19.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


OUT = Path("results/paper_assets")
RLI_DENOMINATOR_FLOOR = 0.05


def add_rli(df: pd.DataFrame, strict_groups: dict) -> pd.DataFrame:
    rows = []
    base = df[df["split"].eq("random")].groupby("model")["mean_pearson"].mean()
    for label, selector in strict_groups.items():
        strict_df = df[selector(df)] if callable(selector) else df[df["split"].eq(selector)]
        strict = strict_df.groupby("model")["mean_pearson"].mean()
        for model in sorted(base.index.intersection(strict.index)):
            random = float(base.loc[model])
            strict_value = float(strict.loc[model])
            rows.append(
                {
                    "strict_label": label,
                    "model": model,
                    "random": random,
                    "strict": strict_value,
                    "LI": random - strict_value,
                    "RLI": (random - strict_value) / random if abs(random) >= RLI_DENOMINATOR_FLOOR else np.nan,
                    "retention": strict_value / random if abs(random) >= RLI_DENOMINATOR_FLOOR else np.nan,
                    "rli_denominator_floor": RLI_DENOMINATOR_FLOOR,
                }
            )
    return pd.DataFrame(rows)


def graph_table() -> pd.DataFrame:
    specs = {
        "Andersson": (
            "results/anderson_graphsage_shared_panel50_trainonly/shared_panel50_graphsage_trainonly_aggregate.csv",
            {"matched_hop0": "matched_hop0", "patient": lambda d: d["split"].str.startswith("patient_")},
        ),
        "Thrane": (
            "results/thrane_graphsage_shared_panel50_trainonly/shared_panel50_graphsage_trainonly_aggregate.csv",
            {"patient": lambda d: d["split"].str.startswith("patient_")},
        ),
        "Visium breast": (
            "results/visium_breast_graphsage_shared_panel50_trainonly/shared_panel50_graphsage_trainonly_aggregate.csv",
            {"matched_hop5": "matched_hop5"},
        ),
    }
    rows = []
    for dataset, (path, strict) in specs.items():
        df = pd.read_csv(path)
        rli = add_rli(df, strict)
        rli.insert(0, "dataset", dataset)
        rli.insert(1, "preprocessing", "train_only_pca_and_scaling")
        rows.append(rli)
    out = pd.concat(rows, ignore_index=True)
    out.to_csv(OUT / "table_graphsage_shared_panel50_RLI_trainonly.csv", index=False)
    return out


def stable_ratio(random_perf: float, strict_perf: float) -> tuple[float, float]:
    if pd.isna(random_perf) or pd.isna(strict_perf) or abs(random_perf) < RLI_DENOMINATOR_FLOOR:
        return np.nan, np.nan
    return (random_perf - strict_perf) / random_perf, strict_perf / random_perf


def mean_moran(path: str) -> float:
    return float(pd.read_csv(path)["moran_i"].head(50).mean())


def two_channel_table(graph: pd.DataFrame) -> pd.DataFrame:
    base = pd.read_csv(OUT / "table_two_channel_leakage.csv")
    base = base[base["model"].ne("graphsage")].copy()
    meta = {
        "Andersson": ("ST_v1", 8, 36, "data/processed/anderson_moran.csv"),
        "Thrane": ("ST_v1", 4, 8, "data/processed/thrane_moran.csv"),
        "Visium breast": ("Visium_breast", 1, 2, "data/processed/visium_breast_moran.csv"),
    }
    rows = []
    for dataset, g in graph.groupby("dataset"):
        spatial = g[g["strict_label"].str.startswith("matched_hop")]
        patient = g[g["strict_label"].eq("patient")]
        random = np.nan
        spatial_strict = np.nan
        patient_strict = np.nan
        if not spatial.empty:
            random = float(spatial["random"].iloc[0])
            spatial_strict = float(spatial["strict"].iloc[0])
        if not patient.empty:
            random = float(patient["random"].iloc[0]) if pd.isna(random) else random
            patient_strict = float(patient["strict"].iloc[0])
        rli_spatial, ret_spatial = stable_ratio(random, spatial_strict)
        rli_patient, ret_patient = stable_ratio(random, patient_strict)
        platform, patients, sections, moran_path = meta[dataset]
        rows.append(
            {
                "dataset": dataset,
                "platform": platform,
                "model": "graphsage_trainonly",
                "random_perf": random,
                "spatial_strict_perf": spatial_strict,
                "patient_strict_perf": patient_strict,
                "RLI_spatial": rli_spatial,
                "RLI_patient": rli_patient,
                "Retention_spatial": ret_spatial,
                "Retention_patient": ret_patient,
                "MoranI": mean_moran(moran_path),
                "patient_count": patients,
                "section_count": sections,
            }
        )
    out = pd.concat([base, pd.DataFrame(rows)], ignore_index=True)
    out.to_csv(OUT / "table_two_channel_leakage_phase19.csv", index=False)
    return out


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    graph = graph_table()
    two = two_channel_table(graph)
    print(graph.round(4).to_string(index=False))
    print(f"wrote {OUT/'table_graphsage_shared_panel50_RLI_trainonly.csv'}")
    print(f"wrote {OUT/'table_two_channel_leakage_phase19.csv'} ({len(two)} rows)")


if __name__ == "__main__":
    main()
