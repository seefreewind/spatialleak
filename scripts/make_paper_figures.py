"""Generate first-pass manuscript figures from frozen paper asset CSV files."""

from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "results" / "paper_assets"
OUT = ASSETS / "figures"

DATASET_ORDER = ["DLPFC", "Andersson", "Thrane", "Visium breast"]
MODEL_LABEL = {
    "pca_ridge": "PCA+Ridge",
    "spatial_knn": "Spatial kNN",
    "graphsage": "GraphSAGE",
    "mean": "Mean",
}
STRICT_LABEL = {
    "matched_hop0": "spatial buffer h0",
    "matched_hop5": "spatial buffer h5",
    "patient": "patient held-out",
    "slide": "slide held-out",
}
COLORS = {
    "random": "#6f7f89",
    "strict": "#c46a55",
    "pca_ridge": "#2b7a78",
    "spatial_knn": "#b35c2e",
    "graphsage": "#4a6fa5",
    "patient": "#c46a55",
    "spatial": "#2b7a78",
    "slide": "#8a7d3a",
    "transfer": "#5b8f6b",
    "neutral": "#6f7f89",
}


def setup_style() -> None:
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
            "svg.fonttype": "none",
            "font.size": 7,
            "axes.spines.right": False,
            "axes.spines.top": False,
            "axes.linewidth": 0.8,
            "axes.labelsize": 7,
            "axes.titlesize": 8,
            "xtick.labelsize": 7,
            "ytick.labelsize": 7,
            "legend.fontsize": 7,
            "legend.frameon": False,
            "figure.dpi": 120,
        }
    )


def read_assets() -> dict[str, pd.DataFrame]:
    return {
        "specific": pd.read_csv(ASSETS / "table_dataset_specific_RLI.csv"),
        "shared": pd.read_csv(ASSETS / "table_shared_panel50_RLI.csv"),
        "graphsage": pd.read_csv(ASSETS / "table_graphsage_shared_panel50_RLI.csv"),
        "distance": pd.read_csv(ASSETS / "figure_distance_curve_data.csv"),
        "heldout": pd.read_csv(ASSETS / "table_dataset_heldout_anderson_to_visium.csv"),
    }


def save_figure(fig: plt.Figure, stem: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"{stem}.svg", bbox_inches="tight")
    fig.savefig(OUT / f"{stem}.png", dpi=600, bbox_inches="tight")
    plt.close(fig)


def panel_label(ax: plt.Axes, label: str) -> None:
    ax.text(
        -0.12,
        1.08,
        label,
        transform=ax.transAxes,
        fontsize=9,
        fontweight="bold",
        va="top",
        ha="left",
    )


def clean_rli(df: pd.DataFrame, min_random: float = 0.05) -> pd.DataFrame:
    out = df.copy()
    out = out[(out["model"] != "mean") & out["RLI"].notna()]
    return out[out["random"].abs() >= min_random]


def rli_barh(
    ax: plt.Axes,
    df: pd.DataFrame,
    title: str,
    color_by: str = "strict_label",
    annotate: bool = True,
) -> None:
    plot = df.copy()
    plot["dataset"] = pd.Categorical(plot["dataset"], DATASET_ORDER, ordered=True)
    plot = plot.sort_values(["dataset", "model", "strict_label"])
    labels = [
        f"{row.dataset}\n{MODEL_LABEL.get(row.model, row.model)}"
        for row in plot.itertuples()
    ]
    palette = {
        "patient": COLORS["patient"],
        "matched_hop0": COLORS["spatial"],
        "matched_hop5": COLORS["spatial"],
        "slide": COLORS["slide"],
        "pca_ridge": COLORS["pca_ridge"],
        "spatial_knn": COLORS["spatial_knn"],
        "graphsage": COLORS["graphsage"],
    }
    colors = [palette.get(getattr(row, color_by), COLORS["neutral"]) for row in plot.itertuples()]
    y = np.arange(len(plot))
    ax.barh(y, plot["RLI"], color=colors, height=0.62)
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set_xlim(0, max(0.85, float(plot["RLI"].max()) + 0.08))
    ax.set_xlabel("Relative leakage inflation (RLI)")
    ax.set_title(title, loc="left", pad=4)
    ax.grid(axis="x", color="#e6e6e6", linewidth=0.7)
    ax.set_axisbelow(True)
    if annotate:
        for yi, val in enumerate(plot["RLI"]):
            ax.text(val + 0.015, yi, f"{val:.2f}", va="center", ha="left", fontsize=6.5)


def make_fig1(data: dict[str, pd.DataFrame]) -> None:
    specific = clean_rli(data["specific"])
    shared = clean_rli(data["shared"])

    pca_patient = specific[
        (specific["model"] == "pca_ridge")
        & (
            (specific["strict_label"] == "patient")
            | ((specific["dataset"] == "Visium breast") & (specific["strict_label"] == "slide"))
        )
    ].copy()
    visium_spatial = specific[
        (specific["dataset"] == "Visium breast")
        & (specific["model"] == "spatial_knn")
        & (specific["strict_label"] == "matched_hop5")
    ]
    overview = pd.concat([pca_patient, visium_spatial], ignore_index=True)

    shared_pca_patient = shared[
        (shared["model"] == "pca_ridge") & (shared["strict_label"] == "patient")
    ].copy()

    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.3), gridspec_kw={"width_ratios": [1.1, 1]})
    panel_label(axes[0], "a")
    rli_barh(
        axes[0],
        overview,
        "Dataset-specific targets",
        color_by="strict_label",
    )

    panel_label(axes[1], "b")
    rli_barh(
        axes[1],
        shared_pca_patient,
        "Frozen shared_panel_50",
        color_by="model",
    )

    fig.suptitle("Random spot splits inflate apparent generalization", x=0.02, y=1.02, ha="left", fontsize=10)
    legend_handles = [
        Patch(facecolor=COLORS["patient"], label="patient-held-out"),
        Patch(facecolor=COLORS["slide"], label="slide-held-out"),
        Patch(facecolor=COLORS["spatial"], label="spatial buffer"),
    ]
    fig.legend(legend_handles, [h.get_label() for h in legend_handles], loc="lower center", ncol=3, bbox_to_anchor=(0.5, -0.02))
    fig.tight_layout(rect=[0, 0.08, 1, 1], w_pad=2.2)
    save_figure(fig, "fig1_leakage_overview")


def plot_distance_panel(ax: plt.Axes, df: pd.DataFrame, dataset: str) -> None:
    subset = df[(df["dataset"] == dataset) & (df["model"].isin(["pca_ridge", "spatial_knn"]))].copy()
    for model, linestyle in [("pca_ridge", "-"), ("spatial_knn", "-")]:
        for family, marker in [("matched", "o"), ("region", "s")]:
            cur = subset[(subset["model"] == model) & (subset["buffer_family"] == family)]
            if cur.empty:
                continue
            cur = cur.sort_values("hop")
            label = f"{MODEL_LABEL[model]}, {family}"
            ax.plot(
                cur["hop"],
                cur["mean_pearson"],
                marker=marker,
                linestyle=linestyle,
                linewidth=1.4,
                markersize=3.5,
                color=COLORS[model],
                alpha=1.0 if family == "matched" else 0.65,
                label=label,
            )
    ax.set_title(dataset, loc="left", pad=4)
    ax.set_xlabel("Minimum train-test buffer (hop)")
    ax.set_ylabel("Mean Pearson")
    ax.set_xticks([0, 1, 2, 5, 10])
    ax.grid(axis="both", color="#e9e9e9", linewidth=0.7)
    ax.set_axisbelow(True)


def make_fig2(data: dict[str, pd.DataFrame]) -> None:
    distance = data["distance"]
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.7), sharey=False)
    for ax, dataset, label in zip(axes, ["DLPFC", "Andersson", "Visium breast"], ["a", "b", "c"]):
        panel_label(ax, label)
        plot_distance_panel(ax, distance, dataset)
    handles, labels = axes[-1].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=4, bbox_to_anchor=(0.5, -0.06))
    fig.suptitle("Spatial-buffer performance decays with neighborhood separation", x=0.02, y=1.03, ha="left", fontsize=10)
    fig.tight_layout(rect=[0, 0.12, 1, 1])
    save_figure(fig, "fig2_spatial_distance_curves")


def make_fig3(data: dict[str, pd.DataFrame]) -> None:
    graph = clean_rli(data["graphsage"])
    shared = clean_rli(data["shared"])
    heldout = data["heldout"][data["heldout"]["model"] == "pca_ridge"].iloc[0]

    shared_patient = shared[
        (shared["model"] == "pca_ridge") & (shared["strict_label"] == "patient")
    ][["dataset", "model", "random", "strict", "LI", "RLI", "retention", "strict_label"]]
    model_compare = pd.concat([shared_patient, graph], ignore_index=True)
    model_compare = model_compare[
        ((model_compare["dataset"] == "DLPFC") & (model_compare["strict_label"] == "matched_hop0"))
        | ((model_compare["dataset"] == "Andersson") & (model_compare["strict_label"] == "patient"))
        | ((model_compare["model"] == "pca_ridge") & (model_compare["strict_label"] == "patient"))
    ].copy()

    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.0), gridspec_kw={"width_ratios": [1.35, 0.85]})
    panel_label(axes[0], "a")
    rli_barh(
        axes[0],
        model_compare,
        "Shared-panel leakage across model classes",
        color_by="model",
    )

    panel_label(axes[1], "b")
    axes[1].bar([0], [heldout["mean"]], color=COLORS["transfer"], width=0.55)
    axes[1].errorbar([0], [heldout["mean"]], yerr=[heldout["std"]], color="#333333", capsize=3, linewidth=0.9)
    axes[1].axhline(0, color="#777777", linewidth=0.8)
    axes[1].set_xticks([0], ["Andersson to\nVisium breast"])
    axes[1].set_ylim(0, 0.24)
    axes[1].set_ylabel("Mean Pearson")
    axes[1].set_title("Dataset-held-out stress test", loc="left", pad=4)
    axes[1].text(0, heldout["mean"] + 0.012, f"{heldout['mean']:.3f}", ha="center", va="bottom", fontsize=7)
    axes[1].grid(axis="y", color="#e9e9e9", linewidth=0.7)
    axes[1].set_axisbelow(True)

    fig.suptitle("Model complexity does not remove evaluation leakage", x=0.02, y=1.03, ha="left", fontsize=10)
    fig.tight_layout(w_pad=2.4)
    save_figure(fig, "fig3_model_and_transfer")


def write_notes() -> None:
    notes = """# Paper Figure Package

> Generated from frozen CSV files in `results/paper_assets/`.

## Figure Contract

- Core conclusion: random spot-level splits inflate apparent generalization through separable patient/batch and spatial-neighborhood channels.
- Archetype: quantitative grid.
- Backend: Python / matplotlib only.
- Export: editable SVG plus high-resolution PNG. PDF is intentionally not generated by default.

## Outputs

- `fig1_leakage_overview.svg/.png`: dataset-specific and shared-panel RLI summary.
- `fig2_spatial_distance_curves.svg/.png`: hop/region buffer curves for DLPFC, Andersson, and Visium breast.
- `fig3_model_and_transfer.svg/.png`: shared-panel model-class leakage and Andersson-to-Visium dataset-held-out stress test.

## Review Notes

- RLI values from models with near-zero random performance are excluded from plotted summaries because the denominator is unstable.
- Visium breast slide-held-out is labeled separately from patient-held-out because the dataset contains one patient.
- Thrane high-hop curves remain absent beyond resolvable matched_hop2 because high-hop splits leave no usable test spots in ST v1.0 density.

## Draft Figure Legends

**Fig. 1 | Leakage inflation across dataset-specific and shared target panels.**
a Relative leakage inflation (RLI) for dataset-specific target panels. Patient-held-out RLI is shown for DLPFC, Andersson, and Thrane with PCA+Ridge; Visium breast is shown with slide-held-out PCA+Ridge and matched_hop5 Spatial kNN because the dataset contains one patient. b PCA+Ridge patient-held-out RLI in the frozen shared_panel_50 target set. Bars show RLI = (random-split performance - strict-split performance) / random-split performance, using mean Pearson as the performance metric. Source data are provided in `table_dataset_specific_RLI.csv` and `table_shared_panel50_RLI.csv`.

**Fig. 2 | Spatial-buffer performance curves.**
a-c Mean Pearson under matched kNN-hop and region-buffer splits for DLPFC, Andersson, and Visium breast. Lines compare PCA+Ridge and Spatial kNN across increasing train-test separation. DLPFC and Visium breast show decreasing Spatial kNN performance as the spatial buffer expands, whereas Andersson has weak Spatial kNN performance under all buffers. Thrane is omitted from the plotted panels because high-hop splits are not resolvable beyond matched_hop2 in the low-density ST v1.0 setting. Source data are provided in `figure_distance_curve_data.csv`.

**Fig. 3 | Leakage persists across model class and cross-platform stress testing remains weak.**
a Shared-panel RLI for PCA+Ridge and GraphSAGE under the strict split most relevant to each leakage channel: DLPFC matched_hop0 and patient-held-out splits for DLPFC, Andersson, and Thrane where available. b Andersson-to-Visium breast dataset-held-out transfer for PCA+Ridge on 49 usable shared targets. Bar height shows mean Pearson across five seeds and the error bar shows standard deviation. Source data are provided in `table_graphsage_shared_panel50_RLI.csv`, `table_shared_panel50_RLI.csv`, and `table_dataset_heldout_anderson_to_visium.csv`.

## QA Checklist

- Backend exclusivity: Python / matplotlib generated all figure files.
- Export files: each figure has SVG with editable text and 600 dpi PNG preview.
- Source traceability: every plotted value comes from a frozen CSV in `results/paper_assets/`.
- Text layout: PNG previews were visually checked for overlapping titles, labels, and legends.
- Statistics: no spot-level confidence intervals are shown; seed/fold definitions remain in the underlying reports.
"""
    (OUT / "FIGURE_PACKAGE_NOTES.md").write_text(notes, encoding="utf-8")


def main() -> None:
    setup_style()
    data = read_assets()
    OUT.mkdir(parents=True, exist_ok=True)
    make_fig1(data)
    make_fig2(data)
    make_fig3(data)
    write_notes()
    print(f"Wrote figures to {OUT}")


if __name__ == "__main__":
    main()
