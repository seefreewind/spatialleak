# Figure 2 Uncertainty Audit

## Finding

The available frozen outputs provide seed-level standard deviation for random/spatial split summaries and subject-fold dispersion for grouped subject-held-out summaries. Uniform biological-unit 95% bootstrap confidence intervals are not available for every Figure 2 point.

## Decision

Figure 2 reports descriptive ±1 s.d. error bars around paired random and strict-tier points. Random estimates and spatial-buffer strict estimates use s.d. across frozen seeds. Subject-held-out strict estimates use s.d. across held-out patient/donor groups, because these folds are biological groups rather than repeated seeds. `Figure2_SourceData.csv` records Δr, the error-bar unit and n for every point.

## Status

PASS for initial submission; no new bootstrap analysis was run.
