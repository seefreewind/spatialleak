# Claim Wording Lock

## Level A: Strongly Supported

| Claim | Required wording |
|---|---|
| Random spot-level evaluation can inflate apparent predictive performance. | supported across datasets; apparent performance inflation |
| Within-section spatial-neighborhood dependence and patient-associated performance loss are separable evaluation phenomena. | separable evaluation phenomena; distinct channels |
| Evaluation regime affects apparent model advantage. | model comparisons depend on evaluation regime |

## Level B: Moderate

| Claim | Required wording |
|---|---|
| A non-zero spatial buffer can be necessary. | can be necessary; observed in GSE278936 and supported by DLPFC/Visium curves |
| GraphSAGE follows patient-channel sensitivity in tumor datasets. | train-only corrected reruns support this in Andersson and Thrane |

## Level C: Boundary / Exploratory

| Claim | Required wording |
|---|---|
| Spatial kNN near-zero settings | boundary condition; RLI not interpretable |
| Thrane high-hop spatial curves | not resolvable in low-density ST v1.0 geometry |
| Spatial signal surviving strict evaluation | may represent transportable biological signal; interpretation, not causal proof |
| Andersson-to-Visium transfer | supplementary stress test |
