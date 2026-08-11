# SpatialLeak Current Situation — Phase 19

> Date: 2026-08-10  
> Status: **Phase 19 complete; experiments closed; manuscript ready for journal-specific formatting**

## Executive Decision

SpatialLeak has passed the Phase 19 pre-submission hardening gate. No additional dataset, model, SOTA comparison, or large experiment should be added unless a target journal or reviewer explicitly requests it.

The project should now move from analysis expansion to manuscript packaging, repository release, and journal-specific formatting.

## Core Scientific Position

SpatialLeak identifies two distinct sources of apparent generalization in spatial omics prediction:

- **Spatial-neighborhood inflation**: random spot splits can overstate performance when nearby training and test spots share local tissue signal.
- **Patient-associated inflation**: random spot splits can also overstate performance when patient, section, sample, batch, or cohort structure is shared across train and test.

These channels are not interchangeable. Spatial buffers, slide-held-out splits, patient-held-out splits, and dataset-held-out stress tests support different claims and should be labelled accordingly.

## Phase 19 Audit Outcome

- Target-panel audit: **PASS / CASE A**. Moran-ranked target panels define the benchmark task and were not selected by downstream model performance.
- PCA+Ridge preprocessing audit: **PASS**. PCA is fit only on training predictors.
- Spatial kNN audit: **PASS**. Predictions use only training coordinates and training target values.
- GraphSAGE audit: **issue found and resolved**. The previous implementation standardized PCA features using all nodes after train-only PCA. `src/models/graphsage.py` now estimates PCA feature mean and standard deviation from training nodes only.
- Corrected GraphSAGE reruns: completed for Andersson, Thrane, and Visium breast. DLPFC corrected GraphSAGE was attempted but not completed, so V4 does not use DLPFC GraphSAGE as main evidence.
- Fatal flaw gate: **PASS**.
- Submission readiness: **91%**.

## Locked Evidence

Main V4 quantitative anchors:

- Visium breast Spatial kNN spatial hop5 RLI: **0.796**.
- Corrected train-only GraphSAGE patient RLI: **0.695** in Andersson and **0.711** in Thrane.
- GSE278936 PCA+Ridge spatial hop5 RLI: **0.222**.
- Random-size-matched controls show that sample-count reduction alone does not explain the main spatial-buffer losses.

GSE278936 is locked as **spatial-channel external replication only**. It must not be described as clean patient-level validation because the public GEO data contain one section per patient.

## Key Files

- Manuscript V4: `manuscript/SPATIALLEAK_MANUSCRIPT_V4.md`
- Final fatal flaw gate: `docs/reports/FINAL_FATAL_FLAW_GATE.md`
- Submission readiness score: `docs/reports/SUBMISSION_READINESS_SCORE_V2.md`
- Target-panel leakage audit: `docs/reports/TARGET_PANEL_LEAKAGE_AUDIT.md`
- Methods completeness audit: `docs/reports/METHODS_COMPLETENESS_AUDIT.md`
- Final figure lock: `docs/reports/FINAL_FIGURE_LOCK.md`
- Supplement lock: `docs/reports/SUPPLEMENT_FINAL_LOCK.md`
- Repository audit: `docs/reports/PUBLIC_REPOSITORY_AUDIT.md`
- Reference expansion: `docs/reports/REFERENCE_EXPANSION_REPORT.md`
- Corrected Phase 19 leakage table: `results/paper_assets/table_two_channel_leakage_phase19.csv`
- Corrected GraphSAGE table: `results/paper_assets/table_graphsage_shared_panel50_RLI_trainonly.csv`

## Verification

- `python3 scripts/reproduce_paper_assets.py`: **PASS**.
- `python3 -m pytest`: **PASS, 7 tests passed**.
- No long-running GraphSAGE, reproducibility, finalization, or pytest process remains active after Phase 19 verification.

## Remaining User Inputs

Only manuscript-packaging inputs remain:

1. Target journal.
2. Author list and affiliations.
3. Funding, acknowledgements, and competing-interest statements.
4. Public GitHub repository decision.
5. Zenodo or equivalent archival DOI decision.

## Stop Rule

Do not reopen experiments by default. The next work unit should be journal-specific formatting and public-release packaging.
