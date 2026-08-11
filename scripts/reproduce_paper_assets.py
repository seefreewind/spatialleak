#!/usr/bin/env python3
"""Smoke-test reproduction of frozen paper assets.

This intentionally starts from existing processed summary results. It does not
download raw data, preprocess h5ad objects, train models, or run GraphSAGE.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


COMMANDS = [
    [sys.executable, "scripts/build_paper_tables.py"],
    [sys.executable, "scripts/build_two_channel_leakage_table.py"],
    [sys.executable, "scripts/build_phase19_corrected_tables.py"],
    [sys.executable, "scripts/make_paper_figures.py"],
]

EXPECTED = [
    "results/paper_assets/table_dataset_specific_RLI.csv",
    "results/paper_assets/table_shared_panel50_RLI.csv",
    "results/paper_assets/table_graphsage_shared_panel50_RLI_trainonly.csv",
    "results/paper_assets/table_two_channel_leakage_phase19.csv",
    "results/paper_assets/table_random_size_matched_control.csv",
    "results/paper_assets/figure_distance_curve_data.csv",
    "results/paper_assets/figures/fig1_leakage_overview.svg",
    "results/paper_assets/figures/fig2_spatial_distance_curves.svg",
    "results/paper_assets/figures/fig3_model_and_transfer.svg",
]


def main() -> None:
    for cmd in COMMANDS:
        print("+", " ".join(cmd), flush=True)
        subprocess.run(cmd, check=True)
    missing = [p for p in EXPECTED if not Path(p).exists()]
    if missing:
        raise SystemExit("Missing expected paper assets:\n" + "\n".join(missing))
    print("paper asset smoke test PASS")


if __name__ == "__main__":
    main()
