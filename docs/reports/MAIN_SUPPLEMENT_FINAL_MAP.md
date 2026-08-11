# Main Versus Supplement Final Map

## Main Text

| Main item | Reason |
|---|---|
| Two-channel distinction | Central conceptual advance |
| Non-zero spatial buffer result | Distinguishes hop0 from meaningful local isolation |
| Patient-held-out channel | Separates patient-associated structure from within-section spatial separation |
| Model-regime dependence | Shows model advantage depends on evaluation tier |
| Six-tier evidence hierarchy | Generalizes the contribution beyond the benchmark tables |

## Supplementary Information

| Supplement item | Reason |
|---|---|
| Cross-platform Pearson 0.199 | Stress test, not central validation |
| Per-gene tables | Too granular for main text |
| Seed/fold tables | Reproducibility support |
| Moran outputs | Target-definition and robustness support |
| Mixed-effects full output | Robustness support |
| Sample-size matched control details | Reviewer defense; one main-text sentence sufficient |
| Dataset QC | Reproducibility support |
| Software versions | Reporting requirement |
| GraphSAGE hyperparameter details | Methods support |
| Non-resolvable splits | Boundary conditions |
| Low-signal Spatial kNN rows | Boundary conditions; avoid misleading RLI interpretation |
| Target-panel robustness | Reviewer defense against Moran target enrichment concern |

## Shared-Panel Robustness Defense

The `shared_panel_50` panel was frozen independently of downstream prediction performance. It supports the patient-associated findings and is reported as robustness evidence. It does not eliminate every target-selection concern because dataset-specific Moran panels still define benchmark tasks.
