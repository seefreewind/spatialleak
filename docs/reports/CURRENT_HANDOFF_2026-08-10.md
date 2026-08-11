# Current Handoff

> Generated: 2026-08-10 18:35 CST  
> Project: SpatialLeak  
> Purpose: Short independent handoff note for continuing work  
> Read first with: `CURRENT_STATUS.md`, `ANALYSIS_LOCK.md`, and `docs/reports/PHASE16_CURRENT_STATUS.md`

## 1. One-Line Status

SpatialLeak is now past Phase 16 synthesis: the project has evidence for two leakage channels, a completed GSE278936 admission audit, a completed limited GSE278936 spatial-channel pilot, refreshed GraphSAGE gap results, and reproducible paper asset tables; the next clean action is manuscript drafting and figure/table consolidation.

## 2. Current Decision Boundary

Do **not** start the full GSE278936 benchmark as originally written.

Reason:

- Public GSE278936 has 52 public sections from 52 public patients.
- Patient-held-out and section-held-out are therefore one-to-one in the public GEO subset.
- It can support high-density Visium spatial-neighborhood leakage testing.
- It cannot cleanly separate patient/batch shortcut from section, slide, site, or cohort effects.

Current decision: **weak GO for GSE278936 as spatial-channel external replication only**.

Completed:

- A limited GSE278936 spatial-channel pilot using random, matched_hop0, matched_hop2, and matched_hop5.

Still requires a different manuscript strategy or explicit user approval:

- Treating GSE278936 as a full two-channel benchmark.
- Pursuing restricted EGA validation data.
- Auditing a new public multi-section-per-patient Visium cohort.

## 3. Files Created or Updated in the Latest Work

Reports:

- `docs/reports/VISIUM_PROSTATE_ADMISSION_REPORT.md`
- `docs/reports/GSE278936_SPATIAL_PILOT_CURRENT_STATUS.md`
- `docs/reports/PHASE16_CURRENT_STATUS.md`
- `docs/reports/CURRENT_HANDOFF_2026-08-10.md`

Paper assets:

- `results/paper_assets/table_two_channel_leakage.csv`
- `results/paper_assets/table_gse278936_spatial_pilot_RLI.csv`
- `results/paper_assets/table_graphsage_shared_panel50_RLI.csv`
- `results/paper_assets/PAPER_RESULT_ASSETS.md`

Scripts:

- `scripts/download_gse278936_processed_minimal.py`
- `scripts/preprocess_gse278936_prostate.py`
- `scripts/build_two_channel_leakage_table.py`
- `scripts/run_graphsage_external.py`
- `scripts/benchmark_external.py`

New GraphSAGE result directories:

- `results/thrane_graphsage_shared_panel50/`
- `results/visium_breast_graphsage_shared_panel50/`

GSE278936 audit data:

- `data/external_audit/gse278936/public_sample_audit.csv`
- `data/external_audit/gse278936/shared_panel_50_gse278936_usable_ensg.csv`
- `data/external_audit/gse278936/shared_panel_50_gse278936_usable_symbols.csv`

GSE278936 processed/pilot outputs:

- `data/processed/gse278936_prostate_hvg2000.h5ad`
- `data/processed/gse278936_prostate_moran.csv`
- `data/processed/gene_panels/shared_panel_50_gse278936_prostate_targets.csv`
- `results/gse278936_prostate_spatial_pilot/`

## 4. Current Two-Channel Evidence

Main synthesis table:

- `results/paper_assets/table_two_channel_leakage.csv`

Rows currently included:

- DLPFC: PCA+Ridge, Spatial kNN, GraphSAGE
- Andersson: PCA+Ridge, Spatial kNN, GraphSAGE
- Thrane: PCA+Ridge, Spatial kNN, GraphSAGE
- Visium breast: PCA+Ridge, Spatial kNN, GraphSAGE

Key numbers:

| Dataset | Model | Spatial RLI | Patient RLI | Interpretation |
|---|---:|---:|---:|---|
| DLPFC | PCA+Ridge | 0.328 | 0.213 | Both channels present, spatial clearer |
| DLPFC | Spatial kNN | 0.402 | 0.120 | Neighborhood leakage, with retained layer signal |
| DLPFC | GraphSAGE | 0.378 | NA | Graph model sensitive to spatial split |
| Andersson | PCA+Ridge | 0.352 | 0.662 | Strong patient/batch channel |
| Andersson | GraphSAGE | 0.072 | 0.692 | Graph model does not remove patient shortcut |
| Thrane | PCA+Ridge | -0.007 | 0.499 | Patient channel dominates |
| Thrane | GraphSAGE | NA | 0.718 | Strong patient-channel loss |
| Visium breast | PCA+Ridge | 0.259 | NA | Spatial channel only; single patient |
| Visium breast | Spatial kNN | 0.796 | NA | Strong high-density neighborhood leakage |
| Visium breast | GraphSAGE | 0.262 | NA | Graph model also loses under hop5 buffer |

Spatial kNN rows with random performance near zero have RLI/Retention set to `NA` because the relative denominator is unstable.

## 5. GSE278936 Audit Summary

Primary audit report:

- `docs/reports/VISIUM_PROSTATE_ADMISSION_REPORT.md`

Officially verified facts:

- GEO accession: GSE278936.
- Public processed data include 52 Visium samples.
- Public raw sequencing data are restricted.
- Public processed files include matrices, feature files, barcodes, coordinates, scale factors, and tissue images.
- The paper reports 80 fresh-frozen tissue sections from 56 prostatectomy samples, with discovery and validation cohorts.
- Public GEO corresponds to the discovery/metastatic accessible processed data.
- The validation cohort with repeated sections per patient is restricted through EGA.
- shared_panel_50 is technically usable in GSE278936.

Local public sample audit now resolves all GSM IDs:

- 52 rows
- 52 non-missing GSM accessions
- 52 unique public patients
- 52 unique public sections

## 6. GSE278936 Spatial Pilot Summary

Primary pilot report:

- `docs/reports/GSE278936_SPATIAL_PILOT_CURRENT_STATUS.md`

Pilot scope:

- `shared_panel_50`
- Seeds `0,1,2,3,4`
- Mean, PCA+Ridge, Spatial kNN
- random, matched_hop0, matched_hop2, matched_hop5

PCA+Ridge mean Pearson:

| Split | Mean Pearson | RLI vs random |
|---|---:|---:|
| random | 0.374473 | NA |
| matched_hop0 | 0.374584 | -0.000296 |
| matched_hop2 | 0.294437 | 0.213731 |
| matched_hop5 | 0.291516 | 0.221532 |

Interpretation:

- Weak GO for supplementary spatial-channel external replication.
- The distance-response signal appears after hop2/hop5 buffering, not at hop0.
- Spatial kNN is not interpretable for RLI because random performance is below zero.
- Do not call this patient-level validation.

## 7. What Not To Do

Do not:

- Modify frozen LI, RLI, or Retention definitions.
- Re-select shared_panel_50 using test results.
- Claim GSE278936 public data cleanly separates patient from section effects.
- Substitute Visium breast slide-held-out as patient-held-out.
- Interpret RLI/Retention when random performance is near zero.
- Add a large SOTA model set unless the manuscript strategy changes.

## 8. Recommended Next Step

The next clean action is manuscript work:

1. Use `table_two_channel_leakage.csv` as the main synthesis asset.
2. Use `table_gse278936_spatial_pilot_RLI.csv` as supplementary spatial-channel external replication.
3. Start formal manuscript drafting and figure/table consolidation.

## 9. Verification State

Last verified commands:

- `python3 scripts/build_two_channel_leakage_table.py`
- `python3 scripts/preprocess_gse278936_prostate.py`
- `python3 scripts/benchmark_external.py --dataset gse278936_prostate --seeds 0,1,2,3,4 --gene-csv data/processed/gene_panels/shared_panel_50_gse278936_prostate_targets.csv --splits random,matched_hop0,matched_hop2,matched_hop5 --hop-buffers 0,2,5 --out-dir results/gse278936_prostate_spatial_pilot --out-prefix spatial_pilot`
- `python3 -m pytest -q`

Last test result:

- 7/7 tests passed.
