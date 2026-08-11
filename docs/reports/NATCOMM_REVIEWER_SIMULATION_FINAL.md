# Nature Communications Reviewer Simulation Final

## Reviewer 1: Spatial omics expert

| Major question | Risk | Current evidence | Main-text answer | Supplement answer | Residual limitation | Need new experiment? |
|---|---|---|---|---|---|---|
| Why only three model classes? | Medium | Diagnostic baselines plus corrected GraphSAGE | Not an exhaustive leaderboard | Model specification and full result tables | Model breadth remains bounded | NO |
| Is strict-split loss just distribution shift? | High | Tiered split comparisons | Apparent generalization inflation, not causal leakage proof | Language lock and hierarchy | Cannot decompose every cause | NO |
| Was target selection test-informed? | Medium | Target-panel audit | Task definition independent of model performance | Target-panel robustness note | Moran targets use descriptive full-dataset information | NO |
| Does sample size explain buffer loss? | Medium | Random-size-matched controls | Main losses exceed size controls | Supplementary Note 4 | Controls are defensive, not exhaustive | NO |
| Is GraphSAGE corrected? | Medium | Train-only scaling code and reruns | Corrected values used; DLPFC excluded | GraphSAGE table | No corrected DLPFC main evidence | NO |
| Is GSE278936 patient validation? | High | 52 patients / 52 sections public data | Spatial-channel replication only | GSE report | Patient/section effects not separable | NO |
| Are NA values hidden? | Low | Figure 3 matrix | NA shown explicitly | Source Data index | Some tiers unavailable | NO |
| Does the framework generalize beyond gene prediction? | Medium | Evaluation-tier logic | Conceptual extension; empirical demo in gene prediction | Discussion limitations | Other tasks untested | NO |

## Reviewer 2: ML methodology expert

| Major question | Risk | Current evidence | Main-text answer | Supplement answer | Residual limitation | Need new experiment? |
|---|---|---|---|---|---|---|
| Why only three model classes? | Medium | Diagnostic baselines plus corrected GraphSAGE | Not an exhaustive leaderboard | Model specification and full result tables | Model breadth remains bounded | NO |
| Is strict-split loss just distribution shift? | High | Tiered split comparisons | Apparent generalization inflation, not causal leakage proof | Language lock and hierarchy | Cannot decompose every cause | NO |
| Was target selection test-informed? | Medium | Target-panel audit | Task definition independent of model performance | Target-panel robustness note | Moran targets use descriptive full-dataset information | NO |
| Does sample size explain buffer loss? | Medium | Random-size-matched controls | Main losses exceed size controls | Supplementary Note 4 | Controls are defensive, not exhaustive | NO |
| Is GraphSAGE corrected? | Medium | Train-only scaling code and reruns | Corrected values used; DLPFC excluded | GraphSAGE table | No corrected DLPFC main evidence | NO |
| Is GSE278936 patient validation? | High | 52 patients / 52 sections public data | Spatial-channel replication only | GSE report | Patient/section effects not separable | NO |
| Are NA values hidden? | Low | Figure 3 matrix | NA shown explicitly | Source Data index | Some tiers unavailable | NO |
| Does the framework generalize beyond gene prediction? | Medium | Evaluation-tier logic | Conceptual extension; empirical demo in gene prediction | Discussion limitations | Other tasks untested | NO |

## Reviewer 3: Computational genomics expert

| Major question | Risk | Current evidence | Main-text answer | Supplement answer | Residual limitation | Need new experiment? |
|---|---|---|---|---|---|---|
| Why only three model classes? | Medium | Diagnostic baselines plus corrected GraphSAGE | Not an exhaustive leaderboard | Model specification and full result tables | Model breadth remains bounded | NO |
| Is strict-split loss just distribution shift? | High | Tiered split comparisons | Apparent generalization inflation, not causal leakage proof | Language lock and hierarchy | Cannot decompose every cause | NO |
| Was target selection test-informed? | Medium | Target-panel audit | Task definition independent of model performance | Target-panel robustness note | Moran targets use descriptive full-dataset information | NO |
| Does sample size explain buffer loss? | Medium | Random-size-matched controls | Main losses exceed size controls | Supplementary Note 4 | Controls are defensive, not exhaustive | NO |
| Is GraphSAGE corrected? | Medium | Train-only scaling code and reruns | Corrected values used; DLPFC excluded | GraphSAGE table | No corrected DLPFC main evidence | NO |
| Is GSE278936 patient validation? | High | 52 patients / 52 sections public data | Spatial-channel replication only | GSE report | Patient/section effects not separable | NO |
| Are NA values hidden? | Low | Figure 3 matrix | NA shown explicitly | Source Data index | Some tiers unavailable | NO |
| Does the framework generalize beyond gene prediction? | Medium | Evaluation-tier logic | Conceptual extension; empirical demo in gene prediction | Discussion limitations | Other tasks untested | NO |
