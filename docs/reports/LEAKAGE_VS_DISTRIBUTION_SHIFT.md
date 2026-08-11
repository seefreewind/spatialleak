# Leakage Versus Distribution Shift

Date: 2026-08-10

## Why This Matters

Reviewers may argue that strict-split performance loss reflects ordinary distribution shift rather than leakage. The manuscript should avoid overclaiming. SpatialLeak measures evaluation-dependent apparent generalization inflation, not a causal proof that every performance difference is illegal data leakage.

## Definitions

### Leakage

Leakage occurs when train and test samples are nominally separated, but information dependence allows test performance to be overly optimistic for the stated generalization claim. In spatial omics, this dependence can arise from local tissue continuity, adjacent spots, overlapping graph neighborhoods, shared patient identity, section-specific background, batch, or cohort structure.

### Distribution Shift

Distribution shift occurs when the test distribution legitimately differs from the training distribution. Patient-held-out, dataset-held-out, and cross-platform tests often include real biological and technical shifts. A performance decrease under these tests does not prove leakage by itself.

### SpatialLeak Position

SpatialLeak should define LI/RLI as:

> evaluation-dependent apparent generalization inflation: the performance advantage observed under permissive random splits that is reduced under biologically or spatially more independent evaluation.

This lets the manuscript retain the SpatialLeak name while keeping the interpretation precise.

## Language Replacements

| Risky phrase | Preferred phrase |
|---|---|
| leakage magnitude | apparent generalization inflation, unless the dependence mechanism is directly established |
| strict split removes leakage | strict split attenuates permissive-split inflation |
| patient-held-out eliminates confounding | patient-held-out reduces patient-identity dependence but may introduce legitimate distribution shift |
| all spatial models exploit leakage | some model-dataset combinations show spatial-neighborhood inflation |
| spatial autocorrelation causes all performance inflation | spatial autocorrelation is most relevant to the within-section spatial channel |

## How To Frame LI and RLI

Use:

- LI = `Perf_random - Perf_strict`
- RLI = `LI / Perf_random`
- Retention = `Perf_strict / Perf_random`

Interpretation:

- LI/RLI summarize how much random-split performance is not retained under a stricter evaluation regime.
- They do not assign all lost performance to a single causal mechanism.
- When random performance is near zero, RLI is unstable and should be set to NA or left uninterpreted.

## Reviewer Rebuttal Core

The manuscript can say:

> We agree that strict-split loss can include legitimate distribution shift. SpatialLeak is therefore framed as a measure of apparent generalization inflation under permissive evaluation, rather than as a causal decomposition of every performance difference. The key finding is that random spot-level performance is not retained under split designs that better match spatial, patient, or dataset-level generalization claims.

## Implication For Manuscript Claims

Keep the central claim:

> SpatialLeak reveals two distinct sources of apparent generalization: local spatial-neighborhood dependence and patient/batch-associated shortcuts.

Avoid:

> SpatialLeak proves that all strict-split loss is leakage.

