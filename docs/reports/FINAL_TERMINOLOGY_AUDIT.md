# Final Terminology Audit

## Locked Vocabulary

| Term | Use | Avoid |
|---|---|---|
| apparent generalization inflation | Primary interpretation of random-minus-strict performance loss | causal proof of leakage |
| leakage inflation (LI) | Numeric difference `Perf_random - Perf_strict` | leakage rate |
| relative leakage inflation (RLI) | Normalized LI when random performance is interpretable | RLI when random performance is near zero |
| spatial-neighborhood channel | Within-section train-test proximity and local tissue continuity | universal spatial leakage |
| patient/batch-associated channel | Patient, section, sample, batch, and cohort-associated shortcuts | clean causal patient mechanism |
| spatial-channel external replication | GSE278936 public Visium role | patient-level validation |
| section-level transfer | Visium breast slide-held-out role | independent patient validation |
| dataset-held-out stress test | Andersson-to-Visium cross-platform result | definitive external validation |

## High-Risk Terms

- `external validation`: use only for true external dataset stress tests and define the evidence level. Do not use for GSE278936 patient validation.
- `independent`: specify independent dataset, section, patient, or split tier.
- `bias`: use for evaluation bias or optimistic performance estimates, not for unmeasured biological bias.
- `causal`, `proof`, `proves`: avoid for LI/RLI. Replace with `supports`, `indicates`, or `is consistent with`.
- `shortcut`: acceptable for patient/batch-associated predictive structure, but pair with a boundary sentence that it may combine biological and technical components.

## Manuscript Rule

Every Results subsection should start with the question being tested, then report the evidence, then give one bounded interpretation. Avoid long sequences of table values in prose; move dense numbers to source tables or Supplementary Information.
