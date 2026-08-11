# Nature Communications Reviewer Simulation

## Reviewer 1: spatial transcriptomics expert

| Question | Risk | Evidence | Manuscript response | Supplementary support | Need new experiment? |
|---|---|---|---|---|---|
| Are random spot splits actually common and problematic? | Medium | Introduction references and multi-dataset contrasts | Frame as interpretation problem, not universal invalidity | Literature and full split tables | NO |
| Does spatial buffering remove real biology? | Medium | Retention under strict splits; Discussion boundary | Spatial dependence is not inherently leakage | Evidence hierarchy | NO |
| Why use Moran-ranked targets? | Medium | Target-panel audit | Task definition, not model tuning | Target-panel note | NO |
| Is GSE278936 patient validation? | High | 52 patients / 52 sections public data | Spatial-channel replication only | GSE278936 report | NO |
| Why does kNN fail in GSE278936? | Medium | Near-zero random performance | Boundary condition, not failed central claim | Full pilot table | NO |
| Are hop buffers biologically meaningful? | Medium | kNN graph distance | Operational neighborhood isolation | Split implementation note | NO |
| Are Visium breast claims overextended? | Medium | Single patient | Spatial and section-level only | Dataset table | NO |
| Is patient-channel language too strong? | Medium | Patient-held-out drops | Patient-associated, not causal batch effect | Reviewer defense | NO |
| Are source datasets heterogeneous? | Low | Yes | Heterogeneity supports evaluation-tier argument | Dataset QC | NO |
| Are there enough spatial platforms? | Medium | Visium and ST v1.0 | Scope is spatial transcriptomics prediction, not all technologies | Limitations | NO |

## Reviewer 2: computational biology benchmark expert

| Question | Risk | Evidence | Manuscript response | Supplementary support | Need new experiment? |
|---|---|---|---|---|---|
| Why only three model classes? | Medium | Diagnostic baselines plus GraphSAGE | Not a SOTA leaderboard | Model specs | NO |
| Why RLI? | Medium | LI/RLI/retention definitions | Operational split-dependent inflation | Metrics note | NO |
| What about near-zero denominators? | Medium | 0.05 rule | Do not interpret near-zero RLI | Full tables | NO |
| Could sample size explain buffer loss? | Medium | Random-size-matched controls | Main losses exceed size losses | Supplementary Note 5 | NO |
| Are seeds cherry-picked? | Low | Frozen seed sets | No test-based seed selection | Reproducibility audit | NO |
| Are all splits comparable? | Medium | Split audit | They answer different claims | Hierarchy figure | NO |
| Does model ranking change robustly? | Medium | Corrected GraphSAGE and baselines | Evaluation-regime dependence | Figure 5 source data | NO |
| Why Pearson? | Low | Mean per-target Pearson | Prediction association metric; full metrics supplementary | Full metrics | NO |
| Are mixed-effects essential? | Low | Robustness only | Keep supplementary | Mixed-effects outputs | NO |
| Is cross-platform stress weak? | Medium | 0.199 supplementary | Not central evidence | Supplementary Note 7 | NO |

## Reviewer 3: machine-learning evaluation expert

| Question | Risk | Evidence | Manuscript response | Supplementary support | Need new experiment? |
|---|---|---|---|---|---|
| Is this leakage or distribution shift? | High | Split-dependent losses | Use apparent generalization inflation and bounded wording | Claim wording lock | NO |
| Was preprocessing train-only? | Low | Code audit | PCA and scaling fit on train only | Methods audit | NO |
| Was GraphSAGE corrected? | Medium | Phase 19 patch and reruns | Corrected train-only external rows; DLPFC excluded | GraphSAGE table | NO |
| Were targets selected with test labels? | Medium | Target-panel audit | Task definition independent of model performance | Target note | NO |
| Was validation used correctly? | Low | Early stopping on validation | No test checkpointing | Code availability | NO |
| Are transductive graph features leakage? | Medium | No label aggregation | It is the channel being evaluated | Methods | NO |
| Are patient and batch separable? | High | Public metadata limits | Not causally separated | Discussion | NO |
| Does framework generalize beyond gene prediction? | Medium | Conceptual hierarchy | Likely applicable, demonstrated in gene prediction | Limitations | NO |
| Are confidence intervals at spot level? | Low | Slide-level bootstrap | No spot-level pseudoreplication for formal claims | Statistics note | NO |
| Should more SOTA models be added? | Medium | Scope framing | Only if reviewer requests | Experiment lock | NO |
