# Nature Communications Claim-Source Audit

| Location | Claim / number | Frozen source | Status |
|---|---|---|---|
| Abstract | Visium breast Spatial kNN hop5 RLI 0.796 | `table_two_channel_leakage_phase19.csv` | PASS |
| Abstract | Andersson corrected GraphSAGE patient RLI 0.695 | `table_graphsage_shared_panel50_RLI_trainonly.csv` | PASS |
| Abstract | Thrane corrected GraphSAGE patient RLI 0.711 | `table_graphsage_shared_panel50_RLI_trainonly.csv` | PASS |
| Abstract | GSE278936 PCA+Ridge hop5 RLI 0.222 | `table_gse278936_spatial_pilot_RLI.csv` | PASS |
| Results | GSE278936 hop0 unchanged | `table_gse278936_spatial_pilot_RLI.csv` | PASS |
| Discussion | GSE278936 not patient-level validation | `GSE278936_SPATIAL_PILOT_CURRENT_STATUS.md` | PASS |
| Methods | Train-only PCA/scaling | `src/models/pca_ridge.py`, `src/models/graphsage.py` | PASS |

## Old GraphSAGE Number Audit

The old values 0.692 and 0.718 are excluded from V5 manuscript text. Corrected values are 0.695 and 0.711. DLPFC GraphSAGE RLI 0.378 is not used as main V5 evidence because the corrected DLPFC rerun was not completed.
