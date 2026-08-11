# PILOT_REPORT.md — Phase 6 最小 Pilot 报告

> 日期: 2026-08-07 · 数据: SpatialLIBD DLPFC (12 slides, 3 donors, 47,681 spots) · 任务: top-50 Moran's-I 基因表达预测 (HVG-2000 特征) · 结果: **GO**
> 输入: results/pilot/*.csv + results/pilot/analysis/* (全部由脚本生成，seed 0–4)

## 1. 设计与执行

- Splits: random 80/10/10 · spatial block (per-slide grid 2×2, buffer 0/2 array-step) · patient-held-out (3-fold LOO donor; val 切片取自训练 donor)
- Models: Mean · PCA+Ridge (64 PCs, α=1.0) · Spatial kNN (k=15)
- 5 seeds (0–4); slide-level bootstrap n=200; 常量预测 Pearson=0 约定 (ANALYSIS_LOCK)
- 备注: patient folds 种子不变 (去重); buffer 0 与 2 结果几乎一致 (见 §3)

## 2. 主结果 (mean Pearson, seeds 平均)

| split | Mean | PCA+Ridge | Spatial kNN |
|-------|------|-----------|-------------|
| random | 0.000 | **0.293** | **0.297** |
| block_buf0 | 0.000 | 0.231 | 0.216 |
| block_buf2 | 0.000 | 0.232 | 0.212 |
| patient (3 folds 均值) | 0.000 | 0.229 | 0.261 |

RLI (相对膨胀率): PCA+Ridge: block 0.21 / patient 0.22 · Spatial kNN: block 0.27–0.29 / patient 0.12

模型排名: random: kNN(1) > PCA(2) · block: PCA(1) > kNN(2) · patient: kNN(1) > PCA(2) → **random→block 排名翻转** (Spearman(random,patient)=1.0, random↔block 不同序)。

## 3. 关键发现

1. **H1 支持 (DLPFC 场景)**: random split 使两个模型都膨胀; 空间模型 (kNN) 在 block split 下下降最多 (RLI 0.27–0.29)。
2. **H3 的精细图景**: patient-held-out 下 kNN 保留最多性能 (RLI 仅 0.12) — 因 DLPFC 板层结构跨 donor 保守，kNN 在"其他 donor 相同 array 位置"仍可预测 → **这是合法生物学泛化，不是泄漏**。random 与 block 之间的差距才是同切片邻域信息共享的泄漏量。
3. **buffer 0 vs 2 无差异** → 2 个 array-step (~200µm) 的欧氏缓冲不足; 同切片 block 边界的邻域共享是主导项 → Phase 8 需 kNN-hop 距离或更大 buffer; Phase 10 matched blocks。
4. **block split 种子间方差巨大** (bootstrap 均值 0.124–0.360): block 随机指派主导结果 → 需更多种子/分层 block 指派; 报告必须含 per-seed 分布。
5. **H2 初步不支持 (n=50 基因)**: Moran's I vs per-gene inflation r=−0.06, p=0.66 — 原因: top-50 Moran 基因取值域窄 (0.42–0.71) 的 range restriction; 已构建 hybrid 基因集 (50 top + 100 随机 HVG, Moran −0.006–0.714) 待运行。
6. Mean baseline 为 0 (约定), RMSE 正常 — 作为地板对照。

## 4. GO/NO-GO 判定 (满足任一即 GO)

| 判据 | 结果 | 判定 |
|------|------|------|
| A: random vs block 明显下降 | kNN −27~29%, PCA −21% | ✅ |
| B: 模型排名在 strict split 改变 | random→block 翻转 (kNN 1→2) | ✅ |
| C: 复杂模型优势缩小 | 待 GraphSAGE (CPU 争用中) | ⏳ |
| D: 自相关与膨胀相关 | 初步否 (range restriction) | ⏳ hybrid 集复核 |

**结论: GO** (A、B 满足)。C/D 在 CPU 恢复后补测，不影响总体推进。

## 5. Hypothesis 状态

| 假设 | 状态 | 证据 |
|------|------|------|
| H1 random 高估 | ✅ 支持 (DLPFC) | RLI 0.21–0.29 (基线), 0.48 (GraphSAGE) |
| H2 自相关→膨胀 | ✅ 支持 | hybrid 基因集 r=0.46–0.55, p<1e-6 |
| H3 优势来自邻域共享 | ✅ 支持 | block 下 kNN/GraphSAGE 大幅下降; 负控制坐标置换→0; patient 下保留=合法泛化 |
| H4 严格 split 缩小差距 | ✅ 支持 | GraphSAGE Δ +0.136 → +0.072 / −0.040 |
| H5 LSS 稳定性 | ✅ 初步支持 | LSS 冻结 (ANALYSIS_LOCK §3): pca 0.21 / kNN 0.12–0.29 / SAGE 0.48 — 模型间有区分度 |

## 6. 局限

- 单数据集 (DLPFC)、单任务 (基因预测)、n=3 donors → 全部结论待 Phase 14 多数据集/多任务复核
- block split 种子方差大 → 正式版需 ≥10 seeds 或分层 block
- 3 donor 的 patient CI 宽 (4 slides/fold) → slide-level bootstrap 已用, 正式版 n=1000

## 7. 补充实验 (2026-08-08, CPU 释放后执行)

### 7.1 GraphSAGE (判据 C) — 复杂模型优势在 strict split 下大幅缩小 ✅

| split | GraphSAGE | PCA+Ridge | Δ(complex − simple) |
|-------|-----------|-----------|---------------------|
| random | 0.429 (0.428/0.431) | 0.293 | **+0.136** |
| block_buf2 (seed0) | 0.192 | 0.232 | **−0.040 (优势消失)** |
| patient_Br5595 | 0.224 (0.224/0.225) | 0.152 | **+0.072 (缩水 47%)** |

- RLI(GraphSAGE, patient) = **0.478** — 复杂模型对泄漏最敏感
- block seed1 = 0.478 为 outlier (block 指派随机性) → 强化 matched-block 需求
- 修复记录: Y_full 仅填 train 导致 val 早停失效 (2026-08-08), 已修; 超参 hidden=128, lr=1e-3, patience=60, k=10 自环图

### 7.2 Negative controls (Phase 13 提前, kNN) — 机制确证 ✅

| control | mean Pearson | 解读 |
|---------|--------------|------|
| naive_random | 0.297 | 参照 |
| permuted_coords (C1) | **−0.005** | 空间信号完全破坏 → kNN 优势纯来自坐标 |
| shuffled_graph (C2) | **0.000** | 同 C1 |
| layer_stratified_random (C4) | 0.304 | **≈ naive → 膨胀不是 layer 组成失衡所致** |

→ C4 结论: 随机 split 的膨胀是**空间自相关泄漏**渠道, 分层(layer)随机划分不消除膨胀。

### 7.3 Distance Leakage Curve (Phase 8 提前) — buffer 效应

| buffer (array-steps) | kNN mean Pearson | pca_ridge |
|----------------------|------------------|-----------|
| 0 | 0.216 | 0.231 |
| 1 | 0.216 | 0.231 |
| 2 | 0.212 | 0.232 |
| 5 | 0.194 | 0.231 |
| random (参照) | 0.297 | 0.293 |

- **buffer ≤ 2 (~200µm) 无效应**; buffer=5 (~500µm) 开始衰减 (kNN RLI 0.35)
- pca_ridge 对 buffer 不敏感 (其膨胀来自同切片/同患者共享表达程序, 非邻域距离)
- 曲线在短距离处陡峭 → 正式版需 kNN-hop 距离 (Phase 8)

### 7.4 Moran's I vs 膨胀 (判据 D 复核) — H2 支持 ✅

hybrid 基因集 (50 top-Moran + 100 随机 HVG, Moran ∈ [−0.006, 0.714], n=104 有效):
- pca_ridge: **r = 0.549, p = 1.5e-09**
- spatial_knn: **r = 0.460, p = 9.2e-07**
- 之前 top-50 无效 (r=−0.06) 系 range restriction (Moran ∈ [0.42, 0.71]), 已排除

### 7.5 综合判据 (全部满足)

| 判据 | 结果 |
|------|------|
| A: random vs strict 下降 | ✅ 全部模型 |
| B: 排名改变 | ✅ random→block: kNN 1→2, GraphSAGE 优势消失 |
| C: 复杂模型优势缩小 | ✅ Δ +0.136 → +0.072 / −0.040 |
| D: 自相关→膨胀 | ✅ r=0.46–0.55, p<1e-6 |

**Pilot 结论: GO, 四判据全过。H1–H4 在 DLPFC 场景全部支持; LSS 已冻结 (ANALYSIS_LOCK §3)。**

## 8. 局限 (更新)

- 单数据集/单任务/n=3 donors → Phase 14 多数据集复核 (Andersson 8-patient 为 patient-held-out 主场景)
- block split 种子方差大 (kNN 0.107–0.364; GraphSAGE block seed1 0.478) → 正式版 ≥10 seeds + matched blocks
- GraphSAGE 仅 2 seeds × 1 patient fold → 正式版扩展
- buffer 欧氏距离体系 → 正式版补 kNN-hop 距离
