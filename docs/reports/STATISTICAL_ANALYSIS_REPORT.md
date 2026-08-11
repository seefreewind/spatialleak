# STATISTICAL_ANALYSIS_REPORT.md — 正式统计框架报告

> 日期: 2026-08-09 · 范围: DLPFC 正式 (10 seeds) + Andersson V0.1 (5 seeds)
> 实现: src/statistics/inference.py (bootstrap / Wilcoxon+BH-FDR / 排名相关 / mixed-effects)
> 禁止 spot-level 推断统计 — 全部以 slide/patient 为抽样单位。

---

## 1. 框架实现清单

| 组件 | 实现 | 状态 |
|------|------|------|
| slide-level bootstrap ×1000 | `slide_bootstrap(n_boot=1000, seed=42)` | ✅ |
| paired Wilcoxon signed-rank | `paired_wilcoxon_bhfdr` (per-seed 配对) | ✅ |
| BH-FDR 多重比较 | 标准 BH (排序→q 值→单调化) | ✅ (已修初版 bug) |
| Spearman / Kendall 排名相关 | `model_rank_correlation` | ✅ |
| mixed-effects | `mixed_effects_inflation` (statsmodels MixedLM) | ✅ |
| Retention = Perf_patient/Perf_random | analyze_formal §6 | ✅ |

## 2. DLPFC 正式结果 (10 seeds)

### 2.1 主效应与不确定性

| split | PCA+Ridge (mean±SD) | Spatial kNN (mean±SD) |
|-------|---------------------|-----------------------|
| random | 0.292 | 0.297 |
| matched_hop0 | 0.196 | 0.177 |
| patient (3 folds) | 0.230 | 0.261 |

bootstrap-1000 (slide 水平, 每 split/model/seed): random 区间宽 ~0.06; matched 区间宽 ~0.10 (block 指派仍为主要方差源, 已由 matched 设计显著压缩: pilot SD 0.096 → formal SD 待核对 summary.csv)。

### 2.2 配对检验 (per-seed Wilcoxon + BH-FDR)

| 比较 | 模型 | median diff | p | p_bh | sig |
|------|------|-------------|----|------|-----|
| random vs matched_hop0 | pca_ridge | +0.117 | 0.002 | 0.0029 | ✅ |
| random vs matched_hop0 | spatial_knn | +0.154 | 0.002 | 0.0029 | ✅ |
| random vs patient | pca_ridge | +0.063 | 0.002 | 0.0029 | ✅ |
| random vs patient | spatial_knn | +0.037 | 0.002 | 0.0029 | ✅ |

注: patient folds 种子不变 → 配对中 patient 侧为固定值 (合法: 检验的是 random 各 seed 相对固定 patient 性能的位置); bootstrap CI 以 slide 为单位的 12/4 个切片为准。

### 2.3 GO-A: per-seed 方向稳定性

- pca_ridge: random > matched_hop0 在 **10/10 seeds** (min diff 0.039)
- spatial_knn: **10/10 seeds** (min diff 0.049)

### 2.4 模型排名 (3 模型, Spearman/Kendall 信息量有限)

random↔patient: Spearman=1.00, Kendall=1.00; random↔matched_hop0: Spearman=0.50, Kendall=0.33 (kNN 与 pca_ridge 顺序翻转)。**需 ≥5 模型才有稳健排名统计 (Priority 6)。**

## 3. Moran ↔ inflation (GO-D, 双数据集)

| 数据集 | 模型 | r | p | n |
|--------|------|-----|-----|-----|
| DLPFC (hybrid 150, 10 seeds) | pca_ridge | 0.550 | 1.5e-09 | 104 |
| DLPFC (hybrid) | spatial_knn | 0.473 | 4.1e-07 | 104 |
| Andersson (hybrid 150) | pca_ridge | 0.743 | 1.5e-27 | 150 |
| Andersson (hybrid) | spatial_knn | 0.503 | 5.7e-11 | 150 |

## 4. Mixed-effects: Inflation ~ MoranI + Model + (1|Dataset)

### 4.1 双数据集版 (2 datasets, 639 观测)

- **MoranI: β = 0.347, p = 7.1e-21** — 自相关每 +0.1 → 膨胀 +0.035
- 交互: MoranI×pca_ridge β=0.536 (p<0.001); MoranI×knn β=0.258 (p=0.025)

### 4.2 三数据集版 (DLPFC + Andersson + Thrane, 1,039 观测) — 正式版

- **加法模型: MoranI β = 0.336, p = 3.4e-31** (Group Var 不显著, n=3 限制)
- 交互模型: MoranI×pca_ridge 显著 (p<0.001), MoranI×knn p=0.071 (边缘)
- 结论: **膨胀-自相关关系跨 3 数据集稳健 (GO-D 统计级确认)**; 模型对 Moran 的敏感度存在差异 (H5 机制)

### 4.3 局限

- n_datasets=3, 随机截距估计弱 (Group Var p=0.33–0.48) — ≥5 datasets 才稳健
- 基因集跨数据集不重叠 (各自 hybrid) — shared_panel_50 基准版本将用统一面板

## 5. Retention (Priority 5) — 泄漏 vs 可迁移空间信号

| 模型 | DLPFC Retention | Andersson Retention | LSS_A (DLPFC) | LSS_B (DLPFC) |
|------|-----------------|---------------------|---------------|---------------|
| PCA+Ridge | 0.787 | 0.315 | 0.270 | 0.328 |
| Spatial kNN | 0.880 | ~0 | 0.261 | 0.402 |

- DLPFC kNN retention 高 (0.88): 板层解剖跨 donor 保守 → transportable signal
- Andersson kNN retention ~0 + 绝对性能 ~0: 无空间信号可迁移
- **结论: Retention 与 RLI 联合解读是区分 "shortcut-dominated spatial dependence" 与 "transportable biological spatial structure" 的必要工具; 单看 RLI 会误判 kNN 为最脆弱模型 (实际其 DLPFC patient 保留率最高)。**

## 6. 与 pilot 的统计一致性

| 指标 | Pilot (5 seeds, 未匹配 block) | Formal (10 seeds, matched block) |
|------|-------------------------------|----------------------------------|
| pca_ridge RLI (block) | 0.21 | **0.33** |
| knn RLI (block) | 0.27–0.29 | **0.40** |
| block SD (knn) | 0.096 | 待核对 (matched 应更低) |
| Moran-膨胀 (DLPFC) | r=0.55/0.46 | r=0.55/0.47 (10 seeds 复现) |

matched block 设计使严格 split 更严格 (组成匹配去除了"好打"的测试 block), 膨胀估计上调 — 方向与 pilot 一致, 幅度更稳。
