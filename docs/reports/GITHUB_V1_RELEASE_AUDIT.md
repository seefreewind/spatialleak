# GitHub v1.0.0 Release Audit

## Status

READY FOR PUBLIC PUSH.

## Included

README, LICENSE, CITATION.cff, environment files, source code, scripts, configs, tests, frozen paper assets, source-data CSV files, manuscript sources, submission reports and final Word manuscript.

## Excluded by .gitignore

Raw data, processed `.h5ad` objects, local caches, rendered DOCX QA PNGs, logs, TIFF figure exports, notebook checkpoints and operating-system files.

## Secrets

No `.env`, `.pem`, `.key`, `*secret*` or `*token*` files were found. The GitHub token shown by `gh auth status` was masked by the CLI and is not stored in the repository.

## GraphSAGE

The active implementation estimates PCA and scaling from training observations only.
