# Phase 16 Current Status

> Date: 2026-08-10  
> Project: SpatialLeak  
> Scope: Two-channel leakage upgrade, GSE278936 admission audit, and GSE278936 spatial pilot  
> Current decision: **GSE278936 weak GO as spatial-channel external replication only**

## 1. What Changed in Phase 16

Phase 16 reframes the manuscript from a single "random split inflation" story into two leakage channels:

1. **Within-section spatial-neighborhood leakage**: nearby spots share spatial signal and inflate random spot-split estimates.
2. **Patient/batch shortcut leakage**: patient, section, cohort, processing, and batch structure can inflate apparent generalization when splits do not hold out the correct unit.

No frozen LI/RLI/Retention definitions were changed. The shared_panel_50 panel remains frozen and was not selected using test performance.

## 2. GSE278936 Admission Audit

The GSE278936 human prostate Visium dataset was audited before benchmarking. The admission decision was **CONDITIONAL GO**, and the approved limited spatial-channel pilot has now been completed.

Key facts:

- Public GEO data contain 52 processed Visium samples with matrices, barcodes, features, spatial coordinates, scale factors, and images.
- Public sample metadata resolve to 52 patients and 52 sections.
- Each public patient contributes one public section, so patient-held-out is effectively section-held-out in the public GEO portion.
- The paper reports a validation cohort with 32 sections from 8 patients, but the reporting summary places this cohort under restricted EGA access.
- shared_panel_50 is technically usable: 50/50 targets were found by ENSG and by gene symbol in the checked feature file.

Consequence:

- GSE278936 is suitable for an additional high-density Visium **spatial-channel** pilot.
- It is not suitable as the central public proof for clean patient-versus-section separation.
- Priority 2 full benchmark should not run under the original two-channel claim.

Primary report:

- `docs/reports/VISIUM_PROSTATE_ADMISSION_REPORT.md`
- `docs/reports/GSE278936_SPATIAL_PILOT_CURRENT_STATUS.md`

Local audit outputs:

- `data/external_audit/gse278936/public_sample_audit.csv`
- `data/external_audit/gse278936/shared_panel_50_gse278936_usable_ensg.csv`
- `data/external_audit/gse278936/shared_panel_50_gse278936_usable_symbols.csv`

Pilot result:

- `results/gse278936_prostate_spatial_pilot/spatial_pilot_aggregate.csv`
- `results/paper_assets/table_gse278936_spatial_pilot_RLI.csv`

Pilot interpretation:

- PCA+Ridge random mean Pearson: 0.374473.
- PCA+Ridge matched_hop0: 0.374584, RLI -0.000296.
- PCA+Ridge matched_hop2: 0.294437, RLI 0.213731.
- PCA+Ridge matched_hop5: 0.291516, RLI 0.221532.
- Spatial kNN random performance is below zero and should not be used for RLI interpretation.
- Final call: weak GO for spatial-channel external replication, with explicit boundary-condition wording.

## 3. Two-Channel Paper Asset

A new reproducible builder was added:

- `scripts/build_two_channel_leakage_table.py`

It writes:

- `results/paper_assets/table_two_channel_leakage.csv`

CSV fields:

`dataset, platform, model, random_perf, spatial_strict_perf, patient_strict_perf, RLI_spatial, RLI_patient, Retention_spatial, Retention_patient, MoranI, patient_count, section_count`

Current table has 12 rows:

- DLPFC: PCA+Ridge, Spatial kNN, GraphSAGE
- Andersson: PCA+Ridge, Spatial kNN, GraphSAGE
- Thrane: PCA+Ridge, Spatial kNN, GraphSAGE
- Visium breast: PCA+Ridge, Spatial kNN, GraphSAGE

Interpretation rules:

- Visium breast has no patient-held-out value because it is a single-patient two-section dataset. Slide-held-out is not substituted for patient-held-out.
- GraphSAGE currently has DLPFC spatial, Andersson spatial/patient, Thrane patient, and Visium breast matched_hop5 values.
- RLI and Retention are set to `NA` when `abs(random_perf) < 0.05`, because the denominator is too small for a stable relative-loss interpretation.
- MoranI is the dataset-level mean Moran's I across the top 50 rows of the corresponding processed Moran table.

## 4. Current High-Signal Interpretation

The existing results support a two-channel framing:

- DLPFC shows clear within-section spatial loss and moderate patient-held-out loss.
- Andersson shows large patient-channel loss for PCA+Ridge and GraphSAGE, while GraphSAGE spatial hop0 loss is small.
- Thrane supports strong patient-channel loss for PCA+Ridge and GraphSAGE; Spatial kNN is not interpretable because random performance is near zero.
- Visium breast strongly supports high-density spatial-neighborhood leakage for Spatial kNN and also shows GraphSAGE matched_hop5 loss, but cannot support patient-level leakage because it has one patient.

## 5. Recommended Next Move

Do not run the full GSE278936 Priority 2 benchmark.

Recommended path:

1. Keep the new two-channel table as the manuscript-level synthesis asset.
2. Treat GSE278936 only as supplementary spatial-channel external replication.
3. Stop adding datasets unless a reviewer or target-journal strategy specifically requires one.
4. Move to manuscript drafting, figure/table consolidation, and strict wording of dataset roles.

## 6. Verification

- `python3 scripts/run_graphsage_external.py --dataset thrane ... --splits random,patient` completed 5 random seeds and 4 deterministic patient folds.
- `python3 scripts/run_graphsage_external.py --dataset visium_breast ... --splits random,matched_hop5 --matched-hop-values 5` completed 5 seeds.
- `python3 scripts/build_two_channel_leakage_table.py` completed and wrote 12 rows.
- `python3 scripts/benchmark_external.py --dataset gse278936_prostate ...` completed the 5-seed spatial-channel pilot.
- `python3 -m pytest -q` passed: 7/7 tests.
