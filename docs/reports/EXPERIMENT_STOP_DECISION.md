# Experiment Stop Decision

Date: 2026-08-10

## Decision

STOP EXPERIMENTS.

The current evidence is sufficient for a full manuscript draft and pre-submission package. Remaining weaknesses are better handled through precise wording, figure architecture, limitations, and reviewer-facing explanation than through additional unplanned analyses.

## Q1. Current Evidence Sufficient For Manuscript?

Yes.

The manuscript has:

- multiple datasets;
- two platforms;
- spatial-buffer, patient-held-out, slide-held-out, dataset-held-out, and cross-platform stress-test tiers;
- simple baseline, spatial nearest-neighbor probe, and GraphSAGE;
- frozen LI/RLI/retention definitions;
- frozen shared_panel_50;
- GSE278936 independent spatial-channel replication.

## Q2. Any Unresolved Fatal Flaw?

No fatal flaw identified.

Important limitations exist, but they do not invalidate the central claim:

- not every dataset supports every evidence level;
- GSE278936 public data cannot separate patient and section effects;
- Visium breast is single-patient;
- Spatial kNN is not informative in several low-signal settings;
- patient/batch mechanisms cannot always be causally decomposed.

These are boundary conditions for the framework, not fatal flaws.

## Q3. Would Adding Another Dataset Materially Change The Central Claim?

Probably not before submission.

Another dataset could increase breadth, but the central claim already rests on distinct evidence sources:

- spatial channel: DLPFC, Visium breast, GSE278936;
- patient/batch channel: Andersson, Thrane, DLPFC;
- cross-platform stress test: Andersson to Visium breast.

Adding a dataset now risks delaying the manuscript and expanding unresolved preprocessing and split-audit burden.

## Q4. Would Adding More SOTA Models Materially Change The Central Claim?

Not for the current manuscript.

The claim is about evaluation design, not winning a model leaderboard. PCA+Ridge, Spatial kNN, and GraphSAGE already cover:

- strong non-spatial baseline;
- direct spatial-neighborhood probe;
- representative graph model.

More SOTA models would shift the paper toward an implementation contest and require license, hyperparameter, compute, and split-protocol audits.

## Q5. Are Remaining Weaknesses Better Handled By Limitations/Discussion?

Yes.

The main remaining weaknesses are interpretation and framing risks:

- leakage versus distribution shift;
- patient shortcuts versus legitimate patient heterogeneity;
- incomplete evidence levels per dataset;
- GSE278936 role;
- RLI instability with low random performance.

These are best addressed in `LEAKAGE_VS_DISTRIBUTION_SHIFT.md`, `EVIDENCE_HIERARCHY.md`, the Discussion, and reviewer response preparation.

## Explicitly Prohibited Unless Reviewer-Driven

- new disease datasets;
- new shared target panel;
- GSE278936 patient-held-out;
- GSE278936 GraphSAGE;
- EGA restricted cohort;
- new SOTA model zoo;
- new primary metric;
- cherry-picked seed or gene selection;
- sensitivity analyses without clear review value.

