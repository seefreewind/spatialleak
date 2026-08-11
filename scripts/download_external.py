#!/usr/bin/env python3
"""External dataset downloads (Phase 7A admission, all URLs verified 2026-08-07/08):

D2 Andersson HER2+ breast (Zenodo 10.5281/zenodo.4751624, password zNLXkYk3Q9znUseS,
   CC BY 4.0): count-matrices.zip (37 MB) + spot-selections.zip + meta.zip
D4 Thrane melanoma (spatialresearch.org, 6.2 MB)
D3 10x Visium breast v1.1.0 (2 sections, CC BY 4.0)

Usage: python scripts/download_external.py [--all|--anderson|--thrane|--visium-breast]
"""
import argparse
import hashlib
import json
import subprocess
import sys
import time
import urllib.request
import zipfile
from pathlib import Path

ZENODO = "https://zenodo.org/records/4751624/files"
ANDERSON_PW = "zNLXkYk3Q9znUseS"
THRANE_URL = "https://www.spatialresearch.org/wp-content/uploads/2019/03/ST-Melanoma-Datasets_1.zip"
VISIUM = [
    ("V1_Breast_Cancer_Block_A_Section_1", "https://cf.10xgenomics.com/samples/spatial-exp/1.1.0/V1_Breast_Cancer_Block_A_Section_1/V1_Breast_Cancer_Block_A_Section_1_filtered_feature_bc_matrix.tar.gz"),
    ("V1_Breast_Cancer_Block_A_Section_1", "https://cf.10xgenomics.com/samples/spatial-exp/1.1.0/V1_Breast_Cancer_Block_A_Section_1/V1_Breast_Cancer_Block_A_Section_1_spatial.tar.gz"),
    ("V1_Breast_Cancer_Block_A_Section_2", "https://cf.10xgenomics.com/samples/spatial-exp/1.1.0/V1_Breast_Cancer_Block_A_Section_2/V1_Breast_Cancer_Block_A_Section_2_filtered_feature_bc_matrix.tar.gz"),
    ("V1_Breast_Cancer_Block_A_Section_2", "https://cf.10xgenomics.com/samples/spatial-exp/1.1.0/V1_Breast_Cancer_Block_A_Section_2/V1_Breast_Cancer_Block_A_Section_2_spatial.tar.gz"),
]


def fetch(url, dest):
    if dest.exists() and dest.stat().st_size > 0:
        print(f"  skip {dest.name} (exists)")
        return
    print(f"  {dest.name} <- {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"})
    with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as f:
        f.write(r.read())


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def anderson(out: Path):
    out.mkdir(parents=True, exist_ok=True)
    for fn in ["count-matrices.zip", "spot-selections.zip", "meta.zip"]:
        dest = out / fn
        fetch(f"{ZENODO}/{fn}?download=1", dest)
        if not dest.exists() or dest.stat().st_size == 0:
            raise RuntimeError(f"download failed: {fn}")
        # encrypted zip: verify password opens it
        with zipfile.ZipFile(dest) as z:
            first = z.namelist()[0]
            if z.getinfo(first).flag_bits & 0x1:  # encrypted
                subprocess.run(["unzip", "-P", ANDERSON_PW, "-l", str(dest)],
                               check=True, capture_output=True)
                print(f"  {fn}: encrypted zip, password OK (n_files={len(z.namelist())})")
            else:
                print(f"  {fn}: NOT encrypted? n_files={len(z.namelist())}")


def thrane(out: Path):
    out.mkdir(parents=True, exist_ok=True)
    dest = out / "ST-Melanoma-Datasets_1.zip"
    fetch(THRANE_URL, dest)
    with zipfile.ZipFile(dest) as z:
        print(f"  files: {z.namelist()[:10]}")


def visium_breast(out: Path):
    out.mkdir(parents=True, exist_ok=True)
    for sample, url in VISIUM:
        fn = url.rsplit("/", 1)[-1]
        dest = out / f"{sample}_{fn}"
        fetch(url, dest)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--anderson", action="store_true")
    ap.add_argument("--thrane", action="store_true")
    ap.add_argument("--visium-breast", action="store_true")
    args = ap.parse_args()
    base = Path("data/raw")
    t0 = time.time()
    if args.all or args.anderson:
        print("== Andersson HER2+ =="); anderson(base / "anderson_her2")
    if args.all or args.thrane:
        print("== Thrane melanoma =="); thrane(base / "thrane_melanoma")
    if args.all or args.visium_breast:
        print("== 10x Visium breast v1.1.0 =="); visium_breast(base / "visium_breast")
    print(f"\nDone in {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
