# Nature Communications Editorial Triage Simulation

## Q1. What is the conceptual advance?

SpatialLeak reframes spatial omics benchmarking as a hierarchy of generalization claims and shows that local spatial and patient-associated inflation are distinct.

## Q2. Why is this more than a benchmark paper?

The manuscript does not rank methods. It changes how benchmark evidence is interpreted by mapping split designs to claims.

## Q3. Why should a broad spatial-omics reader care?

Many spatial omics papers report predictive performance from random spot splits. The framework tells readers what such performance can and cannot establish.

## Q4. Does the study establish a field-level issue?

Yes, with public datasets across brain, breast cancer, melanoma and prostate Visium settings, while keeping claims bounded.

## Q5. Are there enough independent datasets?

Likely enough for a methods/evaluation contribution. Dataset heterogeneity is a strength for the conceptual claim but requires careful boundaries.

## Q6. Are only three model classes a fatal weakness?

No. The model set is diagnostic, not a SOTA leaderboard. The manuscript should keep this framing prominent.

## Q7. Why is the non-zero buffer finding important?

It shows that non-overlapping spatial partitions can still leave local neighborhood dependence, so split labels need distance definitions.

## Q8. Does patient-held-out loss simply reflect distribution shift?

It may include distribution shift. The manuscript frames it as patient-associated performance inflation rather than causal leakage.

## Q9. Are claims appropriately bounded?

Yes, if V5 avoids clean patient-validation language for GSE278936 and avoids treating all strict-split loss as invalid signal.

## Q10. Would this likely be sent for peer review?

Likely yes, if the conceptual hierarchy is made unmistakable and figures are clean.

Desk reject risk: **Moderate**.

Top rejection risks: perceived as a small benchmark; limited SOTA model breadth; final figures not yet publication-polished.

Best risk reductions without new experiments: lead with evidence hierarchy; move low-value details to Supplement; make GraphSAGE correction and dataset boundaries explicit.
