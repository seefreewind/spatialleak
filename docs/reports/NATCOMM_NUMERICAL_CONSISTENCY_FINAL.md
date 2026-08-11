# Nature Communications Numerical Consistency Final

## Numeric sweep

Numbers found in V6:

```text
0.05, 0.222, 0.499, 0.662, 0.695, 0.711, 0.796
```

## Locked anchors

| Number | Meaning | Source | Status |
|---|---|---|---|
| 0.796 | Visium breast Spatial kNN hop5 RLI | `table_two_channel_leakage_phase19.csv` | PASS |
| 0.695 | Andersson corrected GraphSAGE patient RLI | `table_graphsage_shared_panel50_RLI_trainonly.csv` | PASS |
| 0.711 | Thrane corrected GraphSAGE patient RLI | `table_graphsage_shared_panel50_RLI_trainonly.csv` | PASS |
| 0.222 | GSE278936 PCA+Ridge hop5 RLI | `table_gse278936_spatial_pilot_RLI.csv` | PASS |
| 0.199 | Cross-platform stress-test Pearson | Supplement only; not in V6 main text | PASS |

Old GraphSAGE values 0.692 and 0.718 are absent from V6 main text.
