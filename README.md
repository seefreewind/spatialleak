# SpatialLeak

SpatialLeak is an evaluation framework for spatial omics prediction that matches benchmark design to the level of generalization being claimed.

## Why SpatialLeak?

Random spot-level splits test local interpolation. They do not by themselves establish spatial transfer, section transfer, patient transfer or dataset transfer. SpatialLeak compares random splits with spatial buffers, section-held-out, patient-held-out and dataset-held-out regimes to separate local spatial-neighborhood dependence from patient-associated structure.

## Reproduce paper figures

From an environment with the processed result assets available:

```bash
python3 scripts/reproduce_paper_assets.py
```

This regenerates frozen paper tables and figure assets under `results/paper_assets/`.

## Run tests

```bash
python3 -m pytest
```

## Evaluation tiers

| Level | Tier | Supports | Does not establish |
|---:|---|---|---|
| 0 | Random spot interpolation | local interpolation | spatial, section, patient or dataset transfer |
| 1 | Buffered spatial transfer | local neighborhood separation | patient transfer |
| 2 | Section-held-out transfer | section transfer | patient transfer unless patient identity is separated |
| 3 | Patient-held-out transfer | retention across patient-associated groups | dataset or platform transfer |
| 4 | Dataset-held-out transfer | dataset transportability stress test | cross-platform transfer |
| 5 | Cross-platform transfer | robustness across measurement platforms | universal generalization |

## Data availability

The manuscript uses public DLPFC, Andersson HER2-positive breast cancer, Thrane melanoma, 10x Visium breast cancer and GSE278936 prostate Visium data. Restricted EGA validation data were not used.

## Citation

Software archive DOI: https://doi.org/10.5281/zenodo.21881438.


## Repository layout

- `src/`: split generation, models, metrics and statistics.
- `scripts/`: reproducibility and submission-package scripts.
- `configs/`: frozen experiment configuration files.
- `results/paper_assets/`: frozen paper tables and figure source assets.
- `submission/nature_communications/source_data/`: clean source-data files for submission figures.
- `tests/`: unit tests for split/model/metric behavior.

## Datasets

Raw and processed spatial transcriptomics data are not committed to GitHub. Download public datasets from the DLPFC/SpatialLIBD resources, Andersson Zenodo DOI `10.5281/zenodo.4751624`, Thrane melanoma source data, 10x Genomics Visium breast public datasets and GEO accession `GSE278936`. Restricted EGA data were not used.

## Release

Public repository: https://github.com/seefreewind/spatialleak
Version: v1.0.0
Zenodo DOI: https://doi.org/10.5281/zenodo.21881438
