# Nature Communications Figure Plan Final

## Figure 1 - Conceptual framework

**Message:** Evaluation design determines the level of generalization that can be claimed.

Panels: random spot split; spatial-neighborhood dependence; patient-associated structure; evaluation hierarchy; transportable biological signal. Spatial signal must be shown as potentially legitimate when retained under the relevant strict split.

## Figure 2 - Cross-dataset inflation

**Message:** Random spot-level evaluation overstates apparent predictive generalization across multiple dataset-model settings. Use a paired effect plot plus compact forest-style summaries, not a dense heatmap.

## Figure 3 - Two-channel generalization landscape

**Message:** Spatial-channel and patient-channel RLI vary independently. Plot spatial RLI against patient RLI where both are available or use a two-column channel matrix. NA must be visibly NA, never zero.

## Figure 4 - Non-zero buffer

**Message:** Non-overlapping spatial partitions may be insufficient; non-zero exclusion buffers can reveal local neighborhood dependence. Include DLPFC, Visium breast and GSE278936. Put random-size-matched controls in an inset only if readable; otherwise Supplementary Information.

## Figure 5 - Evaluation-regime-dependent model behavior

**Message:** Apparent model advantage depends on random, spatial strict and patient strict evaluation regimes. Use PCA+Ridge, Spatial kNN and corrected train-only GraphSAGE where available.

## Figure 6 - Generalization evidence hierarchy

**Message:** SpatialLeak maps evaluation tiers to supported claims and residual limitations. Levels: random spot interpolation, buffered spatial transfer, section-held-out transfer, patient-held-out transfer, dataset-held-out transfer and cross-platform transfer.
