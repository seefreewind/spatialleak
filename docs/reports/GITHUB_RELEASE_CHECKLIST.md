# GitHub Release Checklist

## Repository State

- Git repository detected: `no`
- Suggested release tag after repository initialization/cleanup: `v1.0.0`
- No push was performed.

## Large Files

- `data/` is approximately 4.0 GB and should not be committed to a normal GitHub repository.
- `results/` is approximately 97 MB and may need selective inclusion.
- Recommended release strategy: commit source code, configs, manuscript, reports, and small paper asset tables; deposit large processed data and raw-data-derived objects separately.

## Secret/Path Audit

No `.env`, `.pem`, `.key`, `*secret*`, or `*token*` files were detected by the Phase 18 shell audit. Absolute local paths remain in documentation where they record local execution context; remove or generalize them before public release if the repository should be machine-portable.

## Pre-Release Tasks

- Add a top-level reproducibility section to `README.md`.
- Confirm data redistribution rights for 10x Genomics demo files and downloaded public matrices.
- Move large raw/processed data to an external repository or release artifact.
- Add `manuscript/references_master.bib`.
- Confirm author names, affiliations, funding, competing interests, and acknowledgements.
- Create a clean git repository or move this workspace into git before tagging.
