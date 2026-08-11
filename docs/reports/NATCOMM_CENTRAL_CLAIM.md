# Nature Communications Central Claim

## One-Sentence Central Claim

Leakage-resistant evaluation reveals distinct local spatial and patient-associated generalization inflation in spatial omics prediction, requiring evaluation tiers matched to the claim being made.

Word count: 24.

## Three Supporting Claims

1. Non-zero spatial buffers exposed local neighborhood dependence, including Visium breast Spatial kNN hop5 RLI 0.796 and GSE278936 PCA+Ridge hop5 RLI 0.222.
2. Patient-held-out evaluation revealed a distinct patient-associated channel, reproduced by corrected train-only GraphSAGE in Andersson and Thrane.
3. Model advantage changed across split regimes, supporting an evidence hierarchy rather than a single random-split leaderboard.

## Explicit Non-Claims

- SpatialLeak does not prove all random-split performance is leakage.
- SpatialLeak does not claim all strict-split loss is invalid signal.
- Spatial dependence itself is not inherently leakage.
- Patient-held-out loss does not causally identify a specific batch effect.
- GSE278936 is not clean patient-level validation.
- The study is not an exhaustive SOTA leaderboard.
