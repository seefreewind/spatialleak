# Figure 3 Color Encoding Audit

## Issue

Thrane PCA+Ridge has spatial RLI = -0.007. A sequential 0-0.8 color scale can visually flatten this value into the same state as zero.

## Decision

Use positive sequential color for RLI >= 0 and a separate negative/no-inflation cell state for values below zero.

## Implementation

- Positive values are encoded on a 0-0.8 sequential scale.
- Negative values are shown with a distinct pale red hatched cell and the label `<0`.
- NA values are shown with a grey hatched cell and the label `NA`.
- The legend states that NA is not zero and `<0` is not positive inflation.

## Status

PASS for V7.
