#!/usr/bin/env python3
"""Download GSE278936 processed files needed for spatial-channel benchmarking."""
from __future__ import annotations

import argparse
import urllib.request
from pathlib import Path

import pandas as pd


BASE = "https://ftp.ncbi.nlm.nih.gov/geo/samples/{bucket}/{gsm}/suppl/{gsm}_{label}_{kind}"
KINDS = [
    "barcodes.tsv.gz",
    "features.tsv.gz",
    "matrix.mtx.gz",
    "tissue_positions_list.csv.gz",
]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--audit-csv", default="data/external_audit/gse278936/public_sample_audit.csv")
    ap.add_argument("--out-dir", default="data/raw/gse278936_prostate/processed_minimal")
    args = ap.parse_args()

    audit = pd.read_csv(args.audit_csv)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = []
    for rec in audit.to_dict("records"):
        gsm = rec["gsm"]
        label = str(rec["geo_sample_label"]).upper()
        sample_dir = out_dir / f"{gsm}_{label}"
        sample_dir.mkdir(parents=True, exist_ok=True)
        for kind in KINDS:
            name = f"{gsm}_{label}_{kind}"
            dest = sample_dir / name
            bucket = f"{gsm[:-3]}nnn"
            url = BASE.format(bucket=bucket, gsm=gsm, label=label, kind=kind)
            if dest.exists() and dest.stat().st_size > 0:
                print(f"skip {dest}")
            else:
                print(f"download {url}")
                urllib.request.urlretrieve(url, dest)
            manifest.append({
                "gsm": gsm,
                "geo_sample_label": rec["geo_sample_label"],
                "download_label": label,
                "kind": kind,
                "path": str(dest),
                "size_bytes": dest.stat().st_size,
            })
    pd.DataFrame(manifest).to_csv(out_dir / "manifest.csv", index=False)
    print(f"wrote {out_dir / 'manifest.csv'}")


if __name__ == "__main__":
    main()
