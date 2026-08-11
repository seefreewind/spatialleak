#!/usr/bin/env python3
"""Build manuscript-ready result tables and figure source data."""
from pathlib import Path

import numpy as np
import pandas as pd


OUT = Path("results/paper_assets")
OUT.mkdir(parents=True, exist_ok=True)


def add_rli(df: pd.DataFrame, strict_groups: dict) -> pd.DataFrame:
    rows = []
    base = df[df["split"].eq("random")].groupby("model")["mean_pearson"].mean()
    for label, selector in strict_groups.items():
        if callable(selector):
            strict_df = df[selector(df)]
        else:
            strict_df = df[df["split"].eq(selector)]
        strict = strict_df.groupby("model")["mean_pearson"].mean()
        for model in sorted(base.index.intersection(strict.index)):
            b = base.loc[model]
            s = strict.loc[model]
            rows.append({
                "strict_label": label,
                "model": model,
                "random": b,
                "strict": s,
                "LI": b - s,
                "RLI": (b - s) / b if abs(b) > 1e-12 else np.nan,
                "retention": s / b if abs(b) > 1e-12 else np.nan,
            })
    return pd.DataFrame(rows)


def table_dataset_specific():
    specs = {
        "DLPFC": ("results/formal_dlpfc/formal_aggregate.csv",
                 {"matched_hop0": "matched_hop0", "patient": lambda d: d["split"].str.startswith("patient_")}),
        "Andersson": ("results/anderson_formal_external/formal_external_aggregate.csv",
                      {"matched_hop5": "matched_hop5", "patient": lambda d: d["split"].str.startswith("patient_")}),
        "Thrane": ("results/thrane_formal_external/formal_external_aggregate.csv",
                   {"matched_hop2": "matched_hop2", "patient": lambda d: d["split"].str.startswith("patient_")}),
        "Visium breast": ("results/visium_breast_v01/v01_aggregate.csv",
                          {"matched_hop5": "matched_hop5", "slide": lambda d: d["split"].str.startswith("slide_")}),
    }
    rows = []
    for dataset, (path, strict) in specs.items():
        df = pd.read_csv(path)
        rli = add_rli(df, strict)
        rli.insert(0, "dataset", dataset)
        rows.append(rli)
    out = pd.concat(rows, ignore_index=True)
    out.to_csv(OUT / "table_dataset_specific_RLI.csv", index=False)
    return out


def table_shared_panel():
    specs = {
        "DLPFC": "results/formal_dlpfc/formal_aggregate_shared_panel50.csv",
        "Andersson": "results/anderson_shared_panel50/shared_panel50_aggregate.csv",
        "Thrane": "results/thrane_shared_panel50/shared_panel50_aggregate.csv",
    }
    rows = []
    for dataset, path in specs.items():
        df = pd.read_csv(path)
        rli = add_rli(df, {"matched_hop0": "matched_hop0",
                           "patient": lambda d: d["split"].str.startswith("patient_")})
        rli.insert(0, "dataset", dataset)
        rows.append(rli)
    out = pd.concat(rows, ignore_index=True)
    out.to_csv(OUT / "table_shared_panel50_RLI.csv", index=False)
    return out


def table_graphsage():
    specs = {
        "DLPFC": (
            "results/formal_dlpfc/formal_aggregate_graphsage_shared_panel50.csv",
            {"matched_hop0": "matched_hop0"},
        ),
        "Andersson": (
            "results/anderson_graphsage_shared_panel50/shared_panel50_graphsage_aggregate.csv",
            {"matched_hop0": "matched_hop0",
             "patient": lambda d: d["split"].str.startswith("patient_")},
        ),
        "Thrane": (
            "results/thrane_graphsage_shared_panel50/shared_panel50_graphsage_aggregate.csv",
            {"patient": lambda d: d["split"].str.startswith("patient_")},
        ),
        "Visium breast": (
            "results/visium_breast_graphsage_shared_panel50/shared_panel50_graphsage_aggregate.csv",
            {"matched_hop5": "matched_hop5"},
        ),
    }
    rows = []
    for dataset, (path, strict) in specs.items():
        df = pd.read_csv(path)
        rli = add_rli(df, strict)
        rli.insert(0, "dataset", dataset)
        rows.append(rli)
    out = pd.concat(rows, ignore_index=True)
    out.to_csv(OUT / "table_graphsage_shared_panel50_RLI.csv", index=False)
    return out


def distance_curve_data():
    specs = {
        "DLPFC": "results/formal_dlpfc/formal_aggregate.csv",
        "Andersson": "results/anderson_formal_external/formal_external_aggregate.csv",
        "Thrane": "results/thrane_formal_external/formal_external_aggregate.csv",
        "Visium breast": "results/visium_breast_v01/v01_aggregate.csv",
    }
    rows = []
    for dataset, path in specs.items():
        df = pd.read_csv(path)
        keep = df[df["split"].str.startswith(("matched_hop", "region_hop"))].copy()
        keep["dataset"] = dataset
        keep["buffer_family"] = np.where(keep["split"].str.startswith("region"), "region", "matched")
        keep["hop"] = keep["split"].str.extract(r"hop(\d+)").astype(float)
        rows.append(keep)
    out = pd.concat(rows, ignore_index=True)
    out = out.groupby(["dataset", "buffer_family", "hop", "split", "model"], as_index=False)["mean_pearson"].mean()
    out.to_csv(OUT / "figure_distance_curve_data.csv", index=False)
    return out


def dataset_heldout_table():
    df = pd.read_csv("results/dataset_heldout/anderson_to_visium_shared_panel50_aggregate.csv")
    out = df.groupby("model", as_index=False)["mean_pearson"].agg(["mean", "std", "min", "max"]).reset_index()
    out.to_csv(OUT / "table_dataset_heldout_anderson_to_visium.csv", index=False)
    return out


def write_markdown():
    ds = pd.read_csv(OUT / "table_dataset_specific_RLI.csv")
    shared = pd.read_csv(OUT / "table_shared_panel50_RLI.csv")
    sage = pd.read_csv(OUT / "table_graphsage_shared_panel50_RLI.csv")
    held = pd.read_csv(OUT / "table_dataset_heldout_anderson_to_visium.csv")
    def val(frame, dataset, strict_label, model, column="RLI"):
        q = (
            (frame["dataset"] == dataset)
            & (frame["strict_label"] == strict_label)
            & (frame["model"] == model)
        )
        return frame.loc[q, column].iloc[0]

    ds_dlpfc_patient = val(ds, "DLPFC", "patient", "pca_ridge")
    ds_anderson_patient = val(ds, "Andersson", "patient", "pca_ridge")
    ds_thrane_patient = val(ds, "Thrane", "patient", "pca_ridge")
    ds_visium_knn_hop5 = val(ds, "Visium breast", "matched_hop5", "spatial_knn")
    sh_dlpfc_patient = val(shared, "DLPFC", "patient", "pca_ridge")
    sh_anderson_patient = val(shared, "Andersson", "patient", "pca_ridge")
    sh_thrane_patient = val(shared, "Thrane", "patient", "pca_ridge")
    sage_dlpfc_hop0 = val(sage, "DLPFC", "matched_hop0", "graphsage")
    sage_anderson_patient = val(sage, "Andersson", "patient", "graphsage")
    held_pca = held.loc[held["model"] == "pca_ridge", "mean"].iloc[0]
    md = [
        "# Paper Result Assets",
        "",
        "> Generated: 2026-08-09 22:15",
        "",
        "## Primary Tables",
        "",
        "- `table_dataset_specific_RLI.csv`: dataset-specific target results across strict splits.",
        "- `table_shared_panel50_RLI.csv`: unified target-panel results for DLPFC, Andersson, and Thrane.",
        "- `table_graphsage_shared_panel50_RLI.csv`: GraphSAGE shared-panel results.",
        "- `table_two_channel_leakage.csv`: Phase 16 synthesis table separating spatial-neighborhood and patient/batch leakage channels.",
        "- `table_dataset_heldout_anderson_to_visium.csv`: cross-platform dataset-held-out stress test.",
        "- `figure_distance_curve_data.csv`: source data for hop/region distance curves.",
        "",
        "## Suggested Figure Panels",
        "",
        "1. Main leakage summary: PCA+Ridge RLI across DLPFC, Andersson, Thrane, and Visium breast.",
        "2. Spatial-neighborhood channel: kNN/GraphSAGE random vs matched_hop buffers, emphasizing Visium and DLPFC.",
        "3. Patient/batch shortcut channel: shared-panel patient retention for DLPFC vs Andersson/Thrane.",
        "4. Platform contrast: Visium breast random/matched/slide-held-out; Thrane high-hop non-resolvability annotated.",
        "5. Supplement: Andersson→Visium dataset-held-out stress test.",
        "",
        "## High-Signal Numbers",
        "",
        f"- Dataset-specific PCA patient RLI: DLPFC {ds_dlpfc_patient:.3f}, "
        f"Andersson {ds_anderson_patient:.3f}, Thrane {ds_thrane_patient:.3f}.",
        f"- Visium kNN matched_hop5 RLI: {ds_visium_knn_hop5:.3f}.",
        f"- Shared-panel PCA patient RLI: DLPFC {sh_dlpfc_patient:.3f}, "
        f"Andersson {sh_anderson_patient:.3f}, Thrane {sh_thrane_patient:.3f}.",
        f"- GraphSAGE shared-panel RLI: DLPFC matched_hop0 {sage_dlpfc_hop0:.3f}; "
        f"Andersson patient {sage_anderson_patient:.3f}.",
        f"- Andersson→Visium PCA dataset-held-out mean Pearson: {held_pca:.3f}.",
        "",
        "## Cautions",
        "",
        "- Spatial kNN RLI is not interpreted when random performance is near zero.",
        "- Visium breast slide-held-out is a cross-section contrast, not patient-level external validation.",
        "- Dataset-held-out transfer is a stress test; it should be supplementary unless strengthened with additional external datasets.",
    ]
    (OUT / "PAPER_RESULT_ASSETS.md").write_text("\n".join(md) + "\n")


def main():
    table_dataset_specific()
    table_shared_panel()
    table_graphsage()
    distance_curve_data()
    dataset_heldout_table()
    write_markdown()
    print(f"wrote paper assets -> {OUT}")


if __name__ == "__main__":
    main()
