# Phase 17 Current Status

Date: 2026-08-10

## One-Line Status

Phase 17 converted SpatialLeak from an experiment-complete benchmark into a pre-submission manuscript architecture package. Experiments are now closed by default; the next work is target-journal-specific formatting, references, final figures, and author/declaration information.

## Central Claim

SpatialLeak reveals that apparent generalization in spatial omics prediction can arise through at least two distinct channels:

1. within-section spatial-neighborhood leakage;
2. patient/batch shortcuts.

These channels require different evaluation strategies and should not be collapsed into a single "random split leakage" claim.

## Files Created

Architecture and framing:

- `docs/reports/EVIDENCE_HIERARCHY.md`
- `docs/reports/ABSTRACT_ARCHITECTURE.md`
- `docs/reports/FINAL_FIGURE_ARCHITECTURE.md`
- `docs/reports/SUPPLEMENT_ARCHITECTURE.md`
- `docs/reports/TITLE_STRATEGY.md`
- `docs/reports/TARGET_JOURNAL_STRATEGY.md`

Audit and risk control:

- `docs/reports/CLAIM_STATISTICS_AUDIT.md`
- `docs/reports/LEAKAGE_VS_DISTRIBUTION_SHIFT.md`
- `docs/reports/FINAL_CLAIM_EVIDENCE_MAP.md`
- `docs/reports/REVIEWER_ATTACK_SIMULATION.md`
- `docs/reports/EXPERIMENT_STOP_DECISION.md`

Manuscript:

- `manuscript/SPATIALLEAK_MANUSCRIPT_V2.md`

## Experiment Decision

STOP EXPERIMENTS.

Do not add:

- new datasets;
- new shared panels;
- GSE278936 patient-held-out;
- GSE278936 GraphSAGE;
- restricted EGA cohorts;
- new SOTA model zoo;
- new primary metrics;
- optional sensitivity analyses without direct reviewer value.

## Key Manuscript Upgrades

- Evidence hierarchy now distinguishes random, spatial-buffer, slide-held-out, patient-held-out, dataset-held-out, and cross-platform stress-test levels.
- GSE278936 is locked as spatial-channel external replication only.
- Visium breast slide-held-out is explicitly section-level, not patient-level.
- GSE278936 Spatial kNN is treated as a boundary condition because random performance is below zero.
- LI/RLI are framed as apparent generalization inflation, not causal proof that every strict-split loss is leakage.
- Six-result structure is defined and used in manuscript v2.

## Target Journal Direction

Recommended paths:

- Ambitious: Genome Biology.
- Stretch: Nature Communications, only if conceptual figures and two-channel framing are excellent.
- Best methods fit: Bioinformatics.
- Other plausible venues: Briefings in Bioinformatics, Patterns, Journal of Biomedical Informatics.

## Remaining User Inputs

- Target journal.
- Abstract format and word limit.
- Author list and affiliations.
- Funding.
- Competing interests.
- Data/code availability wording or repository plan.
- Whether final submission format should be DOCX or LaTeX.

