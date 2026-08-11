# Final Claim-Evidence Map

Date: 2026-08-10

## Central Claim

SpatialLeak reveals that apparent generalization in spatial omics prediction can arise through at least two distinct channels: within-section spatial-neighborhood leakage and patient/batch shortcuts, which require different leakage-resistant evaluation strategies.

## Claim Map

| Claim | Evidence | Primary figure/table | Evidence status | Wording |
|---|---|---|---|---|
| Random spot splits inflate apparent predictive generalization across spatial omics settings | PCA+Ridge random > patient in DLPFC, Andersson, and Thrane; Visium breast random > spatial hop5 for PCA+Ridge and Spatial kNN | Fig. 2; `table_dataset_specific_RLI.csv`; `FINAL_STATS_REFRESH.md` | Strong | "show" |
| Within-section spatial-neighborhood leakage is detectable with spatial exclusion buffers | DLPFC Spatial kNN RLI 0.402; Visium breast Spatial kNN RLI 0.796; GraphSAGE DLPFC spatial RLI 0.378; GSE278936 PCA hop5 RLI 0.222 | Fig. 4; `table_two_channel_leakage.csv`; `table_gse278936_spatial_pilot_RLI.csv` | Strong with model-specific boundaries | "reveal" / "support" |
| Non-zero exclusion buffers can be necessary | GSE278936 PCA+Ridge random 0.374473, matched_hop0 0.374584, matched_hop2 0.294437, matched_hop5 0.291516 | Fig. 4; `GSE278936_SPATIAL_PILOT_CURRENT_STATUS.md` | Moderate, independent spatial replication | "indicate" |
| Patient-held-out evaluation uncovers a distinct patient/batch shortcut channel | Andersson PCA patient RLI 0.662; Thrane PCA patient RLI 0.499; Andersson GraphSAGE patient RLI 0.692; Thrane GraphSAGE patient RLI 0.718; patient-channel Moran p=0.932 | Fig. 3; `table_two_channel_leakage.csv`; `FINAL_STATS_REFRESH.md` | Strong | "uncovers" |
| Dominant leakage channel varies across datasets and models | DLPFC both channels; Andersson and Thrane patient-dominant; Visium breast spatial-dominant; GSE278936 moderate PCA spatial with kNN boundary | Fig. 3; Fig. 4; Supplementary full table | Strong synthesis | "varies" |
| Apparent model advantage is evaluation-regime dependent | DLPFC GraphSAGE spatial RLI 0.378; Andersson GraphSAGE patient RLI 0.692; Thrane GraphSAGE patient RLI 0.718; Visium breast GraphSAGE spatial RLI 0.262 | Fig. 5; `table_graphsage_shared_panel50_RLI.csv` | Moderate to strong | "depends on" |
| Spatial signal can be transportable rather than leakage | DLPFC Spatial kNN patient retention 0.880; Visium breast slide-held-out retention 0.852; Andersson-to-Visium PCA transfer 0.199 | Discussion; Fig. 6 or Supplementary Fig. 7 | Conceptual support | "may represent" |
| SpatialLeak defines a practical evaluation hierarchy | Formalized Levels 0-5 and dataset assignments | Fig. 6; `EVIDENCE_HIERARCHY.md` | Framework contribution | "proposes" / "defines" |

## Claims To Avoid

- All spatial omics benchmarks are invalid.
- All spatial models exploit leakage.
- Spatial autocorrelation explains all inflation.
- Patient-held-out evaluation completely removes confounding.
- GSE278936 validates patient-level generalization.
- Visium breast slide-held-out is patient-held-out.
- Spatial kNN failed in GSE278936; instead call it a boundary condition.

## Main Versus Supplement

Main:

- Central two-channel claim.
- GSE278936 non-zero-buffer result.
- Model advantage depends on split.
- Evaluation hierarchy.

Supplement:

- Per-gene results.
- All seeds/folds.
- Full GraphSAGE details.
- Dataset-held-out stress-test details.
- Non-resolvable split metadata.

