# Reviewer Attack Simulation

Date: 2026-08-10

## Reviewer 1: Computational Biology Methods Expert

| Question | Risk | Current evidence | More analysis required? | Recommended rebuttal |
|---|---|---|---|---|
| Is this ordinary distribution shift rather than leakage? | High | `LEAKAGE_VS_DISTRIBUTION_SHIFT.md`; split hierarchy; LI/RLI definition | No | Frame LI/RLI as evaluation-dependent apparent generalization inflation, not proof that every loss is illegal leakage. |
| Why Pearson correlation as the main metric? | Medium | Frozen in `ANALYSIS_LOCK.md`; per-gene Pearson common for expression prediction; RMSE also retained | No | Pearson captures target-gene expression pattern prediction; supplementary metrics can be reported from existing outputs. |
| Why shared_panel_50? | Medium | Frozen before performance; selected by HVG intersection and Moran rank, not test performance | No | It controls target-set variation across datasets while preserving dataset-specific panels as parallel evidence. |
| Could spatial block difficulty explain lower performance? | High | Matched block construction balances composition; hop curves and GSE278936 hop0 vs hop2/hop5 separate buffer effect | Optional existing-output visualization | Show split metadata and matched block balancing in Supplement. |
| Does hop buffering simply reduce training sample size? | Medium | Matched design and split metadata record dropped/test sizes | Optional existing-output visualization | Report retained test/train counts and non-resolvable splits; do not overstate causal mechanism. |
| Are LI/RLI stable with low denominator? | High | NA rule when `abs(random_perf) < 0.05`; kNN boundary conditions | No | State denominator rule and keep unstable rows out of RLI claims. |
| Are GraphSAGE results hyperparameter-dependent? | Medium | Fixed lightweight implementation; not a SOTA contest | No | Present GraphSAGE as representative model-class probe; avoid claiming best architecture performance. |
| Why no additional SOTA models? | Medium | Phase 17 stop rule; current claim is evaluation framework | No | Additional SOTA models would require separate auditing and shift the paper away from evaluation design. |
| Is dataset-held-out 0.199 meaningful? | Medium | Mean baseline 0; one-direction stress test | No | Treat as feasibility stress test, supplementary if space is tight. |
| Does mixed-effects modeling overfit with few datasets? | Medium | Boundary noted in `FINAL_STATS_REFRESH.md` | No | Present mixed models as supportive and channel-separating, not definitive causal proof. |

## Reviewer 2: Spatial Transcriptomics Expert

| Question | Risk | Current evidence | More analysis required? | Recommended rebuttal |
|---|---|---|---|---|
| Are spatial autocorrelation and tissue continuity being mislabeled as leakage? | High | Discussion distinction between local dependence and transportable biology | No | Spatial signal is not intrinsically leakage; the concern is mismatch between split design and generalization claim. |
| Why does Visium breast slide-held-out stay high? | Medium | Single patient, adjacent sections, high retention | No | This supports transportable section-level tissue structure, not patient-level validation. |
| Why does GSE278936 not validate patient-level generalization? | High | 52 public patients / 52 sections; restricted validation cohort unused | No | Use GSE278936 only as independent spatial-channel Visium replication. |
| Why does Spatial kNN fail in GSE278936? | Medium | random performance below zero; RLI not interpreted | No | Treat as a model- and dataset-specific boundary condition. |
| Are DLPFC layer signals legitimate biology rather than shortcuts? | Medium | Patient retention high for Spatial kNN; DLPFC patient RLI modest | No | This is why retention is reported alongside RLI. |
| Are ST v1.0 and Visium comparable? | Medium | Platform density differences explicitly discussed | No | Use platform differences as evidence of leakage-channel heterogeneity, not as hidden confounding. |
| Are the target genes biologically meaningful? | Low | Moran-ranked and shared-panel analyses both used | No | Gene biology is not the manuscript's primary claim; target selection is frozen and evaluation-focused. |
| Could tumor heterogeneity explain patient/batch shortcuts? | Medium | Andersson/Thrane patient losses | No | Yes; this is part of patient/sample-associated structure, and the manuscript avoids causal decomposition. |
| Are high-hop splits biologically artificial? | Low | They test local train-test dependence | No | Present as diagnostic stress tests, not the only recommended deployment split. |
| Is this relevant beyond gene prediction? | Medium | Current task is expression prediction | No | Discuss as likely relevant to prediction benchmarks broadly, but limit formal claims to tested tasks. |

## Reviewer 3: Machine Learning Evaluation Expert

| Question | Risk | Current evidence | More analysis required? | Recommended rebuttal |
|---|---|---|---|---|
| Is this leakage or just harder OOD evaluation? | High | Concept file and evidence hierarchy | No | SpatialLeak quantifies apparent generalization inflation under permissive splits; OOD difficulty is acknowledged. |
| Is random split a fair comparator? | Medium | It is the permissive baseline, not recommended deployment evidence | No | Random split remains an internal interpolation check and upper-bound comparator. |
| Does strict split change label distribution? | Medium | Matched block selection balances composition | Optional existing metadata summary | Report balancing metadata in supplement. |
| Why use simple baselines? | Low | PCA+Ridge is strong and interpretable; kNN probes spatial locality | No | Baselines diagnose evaluation design and prevent model leaderboard overinterpretation. |
| Why GraphSAGE but no foundation models? | Medium | Computationally tractable representative graph model | No | The paper is about evaluation regimes; foundation models require a separate audit. |
| Are seed counts sufficient? | Medium | 10 seeds for formal DLPFC/external where applicable, 5 seeds for pilot/GraphSAGE external | No | Use seed/fold plots in supplement; avoid overly precise claims from 5-seed pilots. |
| Are hyperparameters tuned on test data? | Low | `ANALYSIS_LOCK.md` prohibits test tuning; fixed settings | No | State integrity controls and fixed hyperparameters. |
| Are metrics cherry-picked? | Low | mean Pearson frozen; RMSE/Spearman retained in outputs | No | Main metric is pre-specified; supplementary metrics available. |
| Why not use nested cross-validation? | Low | Main issue is split hierarchy, not hyperparameter selection | No | Hyperparameters are fixed to prevent test-set optimization. |
| Is leaderboard instability shown directly? | Medium | GraphSAGE and PCA+Ridge strict retention comparisons | Optional figure redesign | Final Fig. 5 should visualize random-to-strict model changes. |

## Optional Pre-Submission Analyses

Maximum three, all from existing data:

1. Split metadata table: train/test/drop counts across matched buffers, especially GSE278936 and Thrane.
2. Seed/fold distribution panels for main RLI results.
3. Final model ranking/advantage source table for Fig. 5.

No new experiment is required before manuscript v2.

