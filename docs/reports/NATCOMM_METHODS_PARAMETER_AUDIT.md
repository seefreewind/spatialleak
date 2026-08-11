# NATCOMM Methods Parameter Audit

| Component | Frozen parameter/source | V7 status |
|---|---|---|
| Predictor genes | 2000 HVGs excluding targets | Included |
| Target genes | top 50 Moran-ranked genes; shared_panel_50 robustness | Included |
| PCA+Ridge PCs | 64 | Included |
| Ridge alpha | 1.0 | Included |
| PCA fit | training observations only | Included |
| Ridge output | one model per target gene | Included |
| Spatial kNN k | 15 | Included |
| Spatial kNN metric | Euclidean distance in normalized per-slide coordinates | Included |
| Spatial kNN weighting | inverse distance `1/(d + 1e-6)` | Included |
| Spatial kNN neighbor source | training spots only | Included |
| Spatial graph k for GraphSAGE | 10 with self-loops | Included |
| GraphSAGE layers | two GraphSAGE layers | Included |
| GraphSAGE hidden dimension | 128 for formal external runs | Included |
| GraphSAGE optimizer | Adam | Included |
| GraphSAGE learning rate | 1e-3 | Included |
| GraphSAGE weight decay | 1e-4 | Included |
| GraphSAGE epochs | up to 500 | Included |
| GraphSAGE early stopping | validation loss, patience 60 | Included |
| Split ratio | random 80/10/10 | Included |
| Matched block candidates | 300 per seed | Included |
| Spatial buffer graph | within-slide kNN graph, k = 15 | Included |
| Main seeds | 0-9 for main baseline analyses; 0-4 for GSE278936 | Included |
| Bootstrap | slide-level, 1000 replicates where available | Included |
| RLI denominator rule | abs(random Pearson) < 0.05 not interpreted | Included |
