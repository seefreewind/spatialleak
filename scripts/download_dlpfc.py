#!/usr/bin/env python3
"""Download SpatialLIBD DLPFC Visium pilot data (~160 MB, no registration).

Sources (verified 2026-08-07):
  - counts:  https://spatial-dlpfc.s3.us-east-2.amazonaws.com/h5/{S}_filtered_feature_bc_matrix.h5
  - spatial: https://raw.githubusercontent.com/LieberInstitute/HumanPilot/master/10X/{S}/...
  - layers:  https://raw.githubusercontent.com/LieberInstitute/HumanPilot/master/10X/barcode_level_layer_map.tsv

Usage: python scripts/download_dlpfc.py --out data/raw/dlpfc
"""
import argparse
import hashlib
import json
import sys
import time
import urllib.request
from pathlib import Path

SAMPLES = [
    "151507", "151508", "151509", "151510",
    "151669", "151670", "151671", "151672",
    "151673", "151674", "151675", "151676",
]
S3 = "https://spatial-dlpfc.s3.us-east-2.amazonaws.com"
GH = "https://raw.githubusercontent.com/LieberInstitute/HumanPilot/master/10X"


def download(url: str, dest: Path) -> bool:
    if dest.exists() and dest.stat().st_size > 0:
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    print(f"  {dest.name} <- {url}")
    urllib.request.urlretrieve(url, dest)
    return True


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="data/raw/dlpfc")
    ap.add_argument("--samples", default=",".join(SAMPLES), help="comma-separated subset")
    ap.add_argument("--skip-h5", action="store_true", help="skip count matrices")
    args = ap.parse_args()
    out = Path(args.out)
    samples = args.samples.split(",")
    t0 = time.time()

    manifest = {"samples": samples, "files": {}, "date": time.strftime("%Y-%m-%d")}
    for s in samples:
        for kind, url in [
            ("filtered", f"{S3}/h5/{s}_filtered_feature_bc_matrix.h5"),
            ("raw", f"{S3}/h5/{s}_raw_feature_bc_matrix.h5"),
        ]:
            if args.skip_h5:
                continue
            dest = out / "h5" / f"{s}_{kind}_feature_bc_matrix.h5"
            if download(url, dest):
                manifest["files"][str(dest.relative_to(out))] = sha256(dest)
        for kind, fn in [
            ("positions", "tissue_positions_list.txt"),
            ("scalefactors", "scalefactors_json.json"),
        ]:
            dest = out / "spatial" / f"{s}_{fn}"
            if download(f"{GH}/{s}/{fn}", dest):
                manifest["files"][str(dest.relative_to(out))] = sha256(dest)

    layer_dest = out / "barcode_level_layer_map.tsv"
    if download(f"{GH}/barcode_level_layer_map.tsv", layer_dest):
        manifest["files"]["barcode_level_layer_map.tsv"] = sha256(layer_dest)

    with open(out / "MANIFEST.json", "w") as f:
        json.dump(manifest, f, indent=2)
    total = sum(p.stat().st_size for p in out.rglob("*") if p.is_file())
    print(f"\nDone in {time.time()-t0:.0f}s. Total size: {total/1e6:.1f} MB")
    print(f"Checksums: {out/'MANIFEST.json'}")
    sys.exit(0)


if __name__ == "__main__":
    main()
