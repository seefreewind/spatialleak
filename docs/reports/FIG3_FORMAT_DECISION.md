# Figure 3 Format Decision

## Prototypes generated

1. Two-channel matrix: `Figure3_final_matrix.*`
2. Scatter prototype: `Figure3_prototype_scatter.*`

## Decision

**Use the two-channel matrix as the final Figure 3.**

## Rationale

The scatter plot is useful only for rows with both spatial-channel and patient-channel RLI. Several central datasets have a valid value on only one channel: Visium breast and GSE278936 lack patient-channel values, while some low-signal kNN rows are not interpretable. A scatter plot would hide those absences or make them look like missing evidence. The matrix keeps NA visible and prevents NA from being interpreted as zero.

## Interpretation rule

Region labels such as spatial-dominant, patient-dominant and mixed are descriptive annotations only. They do not define a new metric or cutoff.
