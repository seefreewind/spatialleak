# Nature Communications Zenodo Release Plan

## Release

- GitHub tag: `v1.0.0`
- Zenodo archive: create from the public GitHub release after final repository cleanup.
- DOI fields: do not invent; insert the issued DOI in the manuscript, Code Availability, Data Availability, README and CITATION.cff.

## Include

`README.md`, `LICENSE`, `CITATION.cff`, `environment.yml`, `requirements.txt`, `configs/`, `src/`, `scripts/`, `tests/`, frozen target-panel metadata, split metadata where size permits, paper asset tables, figure scripts, final source data and documentation.

## Exclude

Raw data, large processed data unless separately deposited, restricted data, local caches, `.pytest_cache`, `__pycache__`, notebook checkpoints, secrets, tokens and local absolute paths.

## License

Recommended code license: MIT or BSD-3-Clause. Recommended manuscript/source-data license should follow Nature Communications open-access requirements and funder rules, typically CC BY 4.0 for the article.
