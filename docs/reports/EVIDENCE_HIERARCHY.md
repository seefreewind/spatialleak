# Evidence Hierarchy for SpatialLeak

Date: 2026-08-10

## Purpose

This file locks the evidence vocabulary for the Phase 17 manuscript rewrite. The manuscript should not call every strict split "external validation". Each split supports a different level of independence, and each dataset should be described only at the level it actually reaches.

## Hierarchy

| Level | Evaluation design | What it tests | What it does not prove |
|---:|---|---|---|
| 0 | Random spot/cell split | Internal interpolation under permissive sampling | Spatial, patient, section, or dataset independence |
| 1 | Spatially isolated split with non-zero exclusion buffer | Within-section prediction after removing local train-test neighborhood overlap | Patient-level generalization |
| 2 | Section/slide-held-out | Transfer to a held-out section or slide | Patient-level generalization unless patients are also separated |
| 3 | Patient-held-out | Generalization across patient/donor identity and associated batch/sample structure | Cross-dataset or cross-platform generalization |
| 4 | Dataset-held-out | Transfer to an independent dataset | Cross-platform robustness unless the platform also changes |
| 5 | Cross-platform held-out | Transfer across dataset and assay/platform context | Universal clinical or biological validity |

Recommended wording:

- Level 0: "random spot-split performance"
- Level 1: "spatially isolated performance" or "spatial-buffer performance"
- Level 2: "section-held-out" or "slide-held-out performance"
- Level 3: "patient-held-out performance"
- Level 4: "dataset-held-out stress test"
- Level 5: "cross-platform stress test"

Avoid:

- "external validation" for random, matched spatial, or slide-held-out splits.
- "patient validation" for single-patient Visium breast or public GSE278936.
- "leakage removed" for any strict split. Use "attenuated", "reduced", or "tested under stricter separation".

## Dataset Assignment

| Dataset | Platform / setting | Highest supported level | Primary use in manuscript | Boundary |
|---|---|---:|---|---|
| DLPFC | Visium DLPFC; 3 donors, 12 sections | Level 3 | Both spatial-neighborhood and patient/donor separation evidence | GraphSAGE shared-panel patient folds were not rerun in Phase 16; existing dataset-specific GraphSAGE patient result remains secondary |
| Andersson | ST v1.0 HER2+ breast cancer; 8 patients, 36 sections | Level 3 | Patient/batch shortcut channel | Spatial kNN random performance is near zero and should not drive RLI claims |
| Thrane | ST v1.0 melanoma; 4 patients, 8 sections | Level 3 | Patient/batch shortcut channel, especially PCA+Ridge and GraphSAGE | High-hop spatial splits are not resolvable at larger buffers in this low-density geometry |
| Visium breast | 10x public breast Visium; one patient, two sections | Level 2 | Dense-platform spatial-neighborhood leakage and section-level transportability | Slide-held-out is not patient-held-out |
| GSE278936 prostate | Public high-density human Visium prostate; 52 patients / 52 sections | Level 1 for this manuscript | Independent spatial-channel Visium replication | Public patient-held-out and section-held-out cannot be decoupled; restricted validation cohort not used |
| Andersson -> Visium breast | ST v1.0 to 10x Visium breast transfer | Level 5 stress test | Cross-platform feasibility check for PCA+Ridge | One direction, 49 usable shared targets, supplementary stress test only |

## Factual Conflict Resolved From Source File

FACTUAL CONFLICT RESOLVED FROM SOURCE FILE: `CURRENT_STATUS.md`, `PROJECT_STATUS.md`, and `NEXT_ACTIONS.md` stop at Phase 15D and do not include the completed Phase 16 GSE278936 pilot. For Phase 17, the current source of truth is `docs/reports/CURRENT_HANDOFF_2026-08-10.md`, `docs/reports/PHASE16_CURRENT_STATUS.md`, `docs/reports/GSE278936_SPATIAL_PILOT_CURRENT_STATUS.md`, and the frozen CSV files in `results/paper_assets/`.

FACTUAL CONFLICT RESOLVED FROM SOURCE FILE: the requested files `docs/reports/TWO_CHANNEL_LEAKAGE_REPORT.md`, `docs/reports/TWO_CHANNEL_STORYBOARD.md`, and `docs/reports/GSE278936_SPATIAL_PILOT_STATUS.md` were not present. Their roles are covered by `docs/reports/PHASE16_CURRENT_STATUS.md`, `docs/reports/CURRENT_HANDOFF_2026-08-10.md`, `docs/reports/GSE278936_SPATIAL_PILOT_CURRENT_STATUS.md`, `results/paper_assets/table_two_channel_leakage.csv`, and `results/paper_assets/table_gse278936_spatial_pilot_RLI.csv`.

## Manuscript Rule

The Results and legends should explicitly name the evidence level each dataset supports. This prevents the central claim from depending on overstated validation language.

