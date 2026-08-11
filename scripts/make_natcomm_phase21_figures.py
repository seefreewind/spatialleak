#!/usr/bin/env python3
"""Create Phase 21 Nature Communications Figure 1 and Figure 3 assets.

Python/matplotlib is the locked plotting backend for this project.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import patches
import numpy as np
import pandas as pd


OUT = Path("submission/nature_communications/FIGURES")
SOURCE = Path("submission/nature_communications/source_data")
PAPER = Path("results/paper_assets")


mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "font.size": 7,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.7,
    "legend.frameon": False,
})


COL = {
    "train": "#4C78A8",
    "test": "#E45756",
    "neutral": "#5B6570",
    "spatial": "#59A14F",
    "patient": "#B07AA1",
    "signal": "#F2B447",
    "strict": "#2F4858",
    "pale": "#F4F6F8",
    "line": "#A9B2BC",
}


def save_pub(fig: plt.Figure, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for ext in ("svg", "pdf"):
        fig.savefig(OUT / f"{name}.{ext}", bbox_inches="tight")
    fig.savefig(OUT / f"{name}.png", dpi=300, bbox_inches="tight")
    fig.savefig(OUT / f"{name}.tiff", dpi=600, bbox_inches="tight")


def panel_label(ax, label: str) -> None:
    ax.text(-0.03, 1.04, label, transform=ax.transAxes, fontsize=10, fontweight="bold",
            va="bottom", ha="right")


def draw_spot_panel(ax) -> None:
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    panel_label(ax, "a")
    ax.text(0, 1.02, "Permissive evaluation", fontsize=9, fontweight="bold", va="bottom")
    ax.text(0, 0.94, "Random spot split intermingles train and test within the same tissue context",
            fontsize=6.6, color=COL["neutral"], va="top")
    rng = np.random.default_rng(4)
    centers = np.array([[0.30, 0.43], [0.55, 0.60], [0.72, 0.35]])
    pts = []
    for c in centers:
        pts.append(c + rng.normal(scale=0.075, size=(22, 2)))
    pts = np.clip(np.vstack(pts), 0.12, 0.88)
    train = rng.random(len(pts)) > 0.25
    ax.add_patch(patches.FancyBboxPatch((0.10, 0.13), 0.78, 0.68,
                                        boxstyle="round,pad=0.015,rounding_size=0.025",
                                        fc="#FFFFFF", ec=COL["line"], lw=0.8))
    ax.text(0.14, 0.77, "same section / patient", fontsize=6.4, color=COL["neutral"])
    ax.scatter(pts[train, 0], pts[train, 1], s=20, c=COL["train"], edgecolor="white", lw=0.35)
    ax.scatter(pts[~train, 0], pts[~train, 1], s=22, c=COL["test"], edgecolor="white", lw=0.35)
    ax.text(0.14, 0.16, "Observed test performance may combine local,\nsection and patient-associated information.",
            fontsize=6.5, color=COL["neutral"], va="bottom")
    ax.scatter([0.68, 0.76], [0.78, 0.78], s=20, c=[COL["train"], COL["test"]], edgecolor="white", lw=0.35)
    ax.text(0.70, 0.78, "train", fontsize=6, va="center", ha="left")
    ax.text(0.78, 0.78, "test", fontsize=6, va="center", ha="left")


def draw_sources_panel(ax) -> None:
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    panel_label(ax, "b")
    ax.text(0, 1.02, "Sources of apparent performance", fontsize=9, fontweight="bold", va="bottom")
    labels = [
        ("Local\nspatial\ndependence", COL["spatial"], "neighboring spots and\ncellular neighborhoods"),
        ("Patient-\nassociated\nstructure", COL["patient"], "patient, section,\nsample or batch context"),
        ("Transportable\nbiological\nsignal", COL["signal"], "legitimate signal retained\nunder stricter separation"),
    ]
    xs = [0.17, 0.50, 0.83]
    for x, (title, color, desc) in zip(xs, labels):
        ax.add_patch(patches.Circle((x, 0.57), 0.135, fc=color, ec="white", lw=1.2, alpha=0.92))
        ax.text(x, 0.58, title, ha="center", va="center", fontsize=6.2, color="white", fontweight="bold")
        ax.text(x, 0.32, desc, ha="center", va="top", fontsize=6.3, color=COL["neutral"])
    ax.text(0.50, 0.11, "Spatial information itself is not invalid; the split determines what it can support.",
            ha="center", fontsize=6.8, color=COL["strict"], fontweight="bold")


def draw_isolation_panel(ax) -> None:
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    panel_label(ax, "c")
    ax.text(0, 1.02, "Isolation strategies", fontsize=9, fontweight="bold", va="bottom")
    pairs = [
        ("Local spatial dependence", "buffered spatial split", COL["spatial"]),
        ("Section-associated structure", "section-held-out", "#7F7F7F"),
        ("Patient-associated structure", "patient-held-out", COL["patient"]),
        ("Broader dataset dependence", "dataset-held-out", "#4C78A8"),
        ("Platform dependence", "cross-platform", "#F58518"),
    ]
    y = 0.80
    for left, right, color in pairs:
        ax.add_patch(patches.FancyBboxPatch((0.02, y - 0.045), 0.39, 0.07,
                                            boxstyle="round,pad=0.012,rounding_size=0.015",
                                            fc="#FFFFFF", ec=color, lw=1.0))
        ax.text(0.215, y - 0.01, left, ha="center", va="center", fontsize=6.5, color=COL["strict"])
        ax.annotate("", xy=(0.56, y - 0.01), xytext=(0.43, y - 0.01),
                    arrowprops=dict(arrowstyle="->", lw=0.9, color=COL["line"]))
        ax.add_patch(patches.FancyBboxPatch((0.58, y - 0.045), 0.37, 0.07,
                                            boxstyle="round,pad=0.012,rounding_size=0.015",
                                            fc=color, ec=color, lw=0.8, alpha=0.90))
        ax.text(0.765, y - 0.01, right, ha="center", va="center", fontsize=6.5, color="white", fontweight="bold")
        y -= 0.145


def draw_hierarchy_panel(ax) -> None:
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    panel_label(ax, "d")
    ax.text(0, 1.02, "Generalization hierarchy", fontsize=9, fontweight="bold", va="bottom")
    levels = [
        ("0", "Random spot interpolation"),
        ("1", "Buffered spatial transfer"),
        ("2", "Section transfer"),
        ("3", "Patient transfer"),
        ("4", "Dataset transfer"),
        ("5", "Cross-platform transfer"),
    ]
    y0, dy = 0.78, 0.095
    for i, (lvl, lab) in enumerate(levels):
        y = y0 - i * dy
        color = mpl.colors.to_hex(plt.cm.Blues(0.30 + 0.10 * i))
        ax.add_patch(patches.FancyBboxPatch((0.16, y - 0.030), 0.68, 0.058,
                                            boxstyle="round,pad=0.009,rounding_size=0.012",
                                            fc=color, ec="white", lw=1.0))
        ax.text(0.22, y, f"Level {lvl}", ha="center", va="center",
                fontsize=6.3, color="white", fontweight="bold")
        ax.text(0.52, y, lab, ha="center", va="center", fontsize=6.3, color="white")
        if i < len(levels) - 1:
            ax.annotate("", xy=(0.50, y - 0.065), xytext=(0.50, y - 0.034),
                        arrowprops=dict(arrowstyle="->", lw=0.75, color=COL["line"]))
    ax.text(0.50, 0.12, "The evaluation tier determines the level of\ngeneralization that can be claimed.",
            ha="center", va="center", fontsize=8, color=COL["strict"], fontweight="bold")


def make_figure1() -> None:
    fig = plt.figure(figsize=(7.4, 5.4))
    gs = fig.add_gridspec(2, 2, left=0.045, right=0.98, top=0.91, bottom=0.08, wspace=0.20, hspace=0.34)
    fig.suptitle("Evaluation design determines the generalization claim", x=0.045, y=0.985,
                 ha="left", fontsize=11, fontweight="bold")
    draw_spot_panel(fig.add_subplot(gs[0, 0]))
    draw_sources_panel(fig.add_subplot(gs[0, 1]))
    draw_isolation_panel(fig.add_subplot(gs[1, 0]))
    draw_hierarchy_panel(fig.add_subplot(gs[1, 1]))
    save_pub(fig, "Figure1_final")
    plt.close(fig)


def figure3_dataframe() -> pd.DataFrame:
    two = pd.read_csv(PAPER / "table_two_channel_leakage_phase19.csv")
    gse = pd.read_csv(PAPER / "table_gse278936_spatial_pilot_RLI.csv")
    rows = []
    keep = [
        ("DLPFC", "pca_ridge"),
        ("DLPFC", "spatial_knn"),
        ("Andersson", "pca_ridge"),
        ("Andersson", "graphsage_trainonly"),
        ("Thrane", "pca_ridge"),
        ("Visium breast", "pca_ridge"),
        ("Visium breast", "spatial_knn"),
        ("Visium breast", "graphsage_trainonly"),
    ]
    for dataset, model in keep:
        r = two[(two["dataset"] == dataset) & (two["model"] == model)].iloc[0]
        rows.append({
            "dataset": dataset,
            "model": model.replace("_trainonly", " train-only").replace("_", "+").replace("spatial+knn", "Spatial kNN").replace("pca+ridge", "PCA+Ridge"),
            "spatial_RLI": r["RLI_spatial"],
            "patient_RLI": r["RLI_patient"],
            "note": "",
        })
    rg = gse[(gse["model"] == "pca_ridge") & (gse["comparison"] == "random_vs_matched_hop5")].iloc[0]
    rows.append({
        "dataset": "GSE278936",
        "model": "PCA+Ridge",
        "spatial_RLI": rg["rli"],
        "patient_RLI": np.nan,
        "note": "spatial-channel replication only",
    })
    df = pd.DataFrame(rows)
    return df


def make_figure3_matrix(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(6.3, 4.8))
    vals = df[["spatial_RLI", "patient_RLI"]].to_numpy(float)
    masked = np.ma.masked_invalid(vals)
    cmap = mpl.colors.LinearSegmentedColormap.from_list("rli", ["#F6F8FA", "#A8DADC", "#457B9D", "#1D3557"])
    im = ax.imshow(masked, vmin=0, vmax=0.8, cmap=cmap, aspect="auto")
    ylabels = [f"{d} | {m}" for d, m in zip(df["dataset"], df["model"])]
    ax.set_yticks(np.arange(len(df)), ylabels, fontsize=6.5)
    ax.set_xticks([0, 1], ["Spatial-channel RLI", "Patient-associated RLI"], fontsize=7)
    ax.tick_params(length=0)
    for i in range(vals.shape[0]):
        for j in range(vals.shape[1]):
            if np.isfinite(vals[i, j]):
                color = "white" if vals[i, j] > 0.45 else COL["strict"]
                ax.text(j, i, f"{vals[i, j]:.3f}", ha="center", va="center", fontsize=7, color=color, fontweight="bold")
            else:
                ax.add_patch(patches.Rectangle((j - 0.5, i - 0.5), 1, 1, fc="#F1F1F1", ec="white", hatch="///", lw=0.5))
                ax.text(j, i, "NA", ha="center", va="center", fontsize=7, color="#666666")
    for y in np.arange(-0.5, len(df), 1):
        ax.axhline(y, color="white", lw=1)
    ax.axvline(0.5, color="white", lw=1)
    ax.set_title("Dominant inflation channels vary across datasets and models", fontsize=10, fontweight="bold", loc="left", pad=12)
    ax.text(-0.48, -1.18, "a", fontsize=10, fontweight="bold", transform=ax.transData)
    ax.text(-0.47, -0.78, "Descriptive channel map; no cutoff is implied.",
            fontsize=6.5, color=COL["neutral"], transform=ax.transData)
    cbar = fig.colorbar(im, ax=ax, fraction=0.040, pad=0.03)
    cbar.set_label("Relative leakage inflation (RLI)", fontsize=7)
    cbar.ax.tick_params(labelsize=6)
    ax.text(0.5, len(df) + 0.20, "NA means the tier is unavailable or not interpretable; it is not plotted as zero.",
            ha="center", va="top", fontsize=6.5, color=COL["neutral"])
    fig.tight_layout()
    save_pub(fig, "Figure3_final_matrix")
    plt.close(fig)


def make_figure3_scatter(df: pd.DataFrame) -> None:
    both = df[df[["spatial_RLI", "patient_RLI"]].notna().all(axis=1)].copy()
    fig, ax = plt.subplots(figsize=(5.0, 4.4))
    colors = {"DLPFC": "#4C78A8", "Andersson": "#B07AA1", "Thrane": "#7F7F7F"}
    markers = {"PCA+Ridge": "o", "Spatial kNN": "s", "graphsage train-only": "^"}
    for _, r in both.iterrows():
        ax.scatter(r.spatial_RLI, r.patient_RLI, s=58, c=colors.get(r.dataset, "#333333"),
                   marker=markers.get(r.model, "o"), edgecolor="white", lw=0.7, zorder=3)
        ax.text(r.spatial_RLI + 0.015, r.patient_RLI + 0.015, f"{r.dataset}\n{r.model}",
                fontsize=6.1, color=COL["strict"])
    ax.axline((0, 0), slope=1, color=COL["line"], lw=0.9, ls="--")
    ax.set_xlim(-0.03, 0.85)
    ax.set_ylim(-0.03, 0.85)
    ax.set_xlabel("Spatial-channel RLI")
    ax.set_ylabel("Patient-associated RLI")
    ax.set_title("Scatter prototype: interpretable rows with both channels", fontsize=10, fontweight="bold", loc="left")
    ax.text(0.06, 0.76, "patient-dominant", color=COL["patient"], fontsize=7)
    ax.text(0.55, 0.06, "spatial-dominant", color=COL["spatial"], fontsize=7)
    ax.text(0.43, 0.43, "mixed", color=COL["neutral"], fontsize=7)
    fig.tight_layout()
    save_pub(fig, "Figure3_prototype_scatter")
    plt.close(fig)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCE.mkdir(parents=True, exist_ok=True)
    make_figure1()
    df = figure3_dataframe()
    df.to_csv(SOURCE / "Figure3_Final_SourceData.csv", index=False)
    make_figure3_matrix(df)
    make_figure3_scatter(df)
    print("Wrote Nature Communications Phase 21 Figure 1 and Figure 3 assets.")


if __name__ == "__main__":
    main()
