# MULTIDATASET_BENCHMARK_V0.1.md — 跨数据集 Benchmark v0.1

> 日期: 2026-08-09 · 范围: DLPFC (正式版) + Andersson HER2+ (V0.1) 主比较
> 数据: results/formal_dlpfc/ + results/anderson_v01/ (全部脚本生成)

---

## 1. 设计

统一任务: 多基因表达重建 (HVG-2000 特征 → top-50 Moran 靶基因), 指标 mean Pearson (per-gene, spot 水平聚合后 slide 水平 bootstrap)。
模型: Mean / PCA+Ridge / Spatial kNN / (DLPFC 另加 GraphSAGE)。
Splits: random (naive) vs matched spatial block (hop0, 组成匹配) vs patient-held-out。

## 2. 主表 (mean Pearson)

### DLPFC (10 seeds; GraphSAGE 10 seeds 待后台完成, 当前 n=4)

| split | PCA+Ridge | Spatial kNN | GraphSAGE |
|-------|-----------|-------------|-----------|
| random | 0.292 | 0.297 | 0.429 |
| matched_hop0 | 0.196 | 0.177 | 0.241–0.357 (n=4) |
| patient (3 folds 均值) | 0.230 | 0.261 | 0.224–0.460 (fold 间) |

RLI: matched pca 0.328 / knn 0.402; patient pca 0.213 / knn 0.120。

### Andersson HER2+ (5 seeds; 8 patient folds)

| split | PCA+Ridge | Spatial kNN |
|-------|-----------|-------------|
| random | **0.603** | 0.032 |
| matched_hop0 | 0.583 | 0.016 |
| patient (8 folds) | **0.190** (fold 0.13–0.31) | ~0.000 |

RLI: patient pca_ridge = **0.69**; matched pca = 0.03; kNN 无空间信号 (平台差异, 见 §4)。

## 3. 跨数据集一致性 (GO-B / GO-D)

| 观测 | DLPFC | Andersson | Thrane | 一致? |
|------|-------|-----------|--------|-------|
| random > patient (PCA+Ridge) | 0.292→0.230 (RLI 0.21) | 0.603→0.190 (RLI 0.69) | 0.652→0.327 (RLI 0.50) | ✅ **三数据集全过 (GO-B)** |
| Moran-I ↔ per-gene inflation | r=0.55/0.46 (p<1e-6) | **r=0.74/0.50 (p<1e-9)** | 待补 (见下) | ✅ 同向显著 |
| 平均 Moran's I (HVG) | 0.029 | 0.010 | 0.019 | Andersson/Thrane 自相关更弱 |
| spatial kNN 随机 split 绝对性能 | 0.297 | 0.032 | −0.009 | **平台效应: 仅 Visium 密度下 kNN 有信号** |

**关键发现 1 (泄漏双渠道)**: DLPFC 的膨胀主要经"空间邻域共享"渠道 (kNN/GraphSAGE 高敏感); Andersson 的膨胀主要经"患者身份/批次"渠道 (pca_ridge RLI 0.69, 空间模型几乎无信号可泄)。两种渠道都使 random split 失效 — 但机制不同, 论文需分别刻画。

**关键发现 2 (平台效应)**: ST v1.0 低密度 (~300 spots/切片) + 高 dropout → spatial kNN 绝对性能极低 (0.03 vs Visium 0.30); 空间模型的"信息共享收益"在低密度平台几乎不存在。**不能用 RLI 单独比较跨平台模型, 需同时报绝对性能与 Retention。**

## 4. Retention (Priority 5) — 区分泄漏与可迁移空间信号

| 模型 | DLPFC retention (patient/random) | Andersson retention | Thrane retention | 解读 |
|------|----------------------------------|---------------------|------------------|------|
| PCA+Ridge | 0.787 | 0.315 | 0.502 | 非空间模型: patient 下大幅下降 (患者特异性表达程序) |
| Spatial kNN | 0.880 | ~0 | ~0 | DLPFC: kNN 跨 donor 仍可利用保守板层解剖 → **transportable spatial signal**; Andersson/Thrane: 无可迁移信号 |

- DLPFC kNN 的 Retention (0.88) > GraphSAGE (~0.52, n=4 初值) → kNN 依赖的板层结构跨 donor 保守 (合法泛化), GraphSAGE 更依赖同切片邻域 (shortcut 主导)。
- **不要把所有空间相关性定义成 leakage**: DLPFC kNN 的 patient 保留部分 = 可迁移生物学空间结构。

## 5. 模型排名 (DLPFC)

| 排名 | random | matched_hop0 | patient |
|------|--------|--------------|---------|
| 1 | GraphSAGE (0.429) | GraphSAGE (0.28) | GraphSAGE (0.33) |
| 2 | kNN (0.297) | pca_ridge (0.196) | kNN (0.261) |
| 3 | pca_ridge (0.292) | kNN (0.177) | pca_ridge (0.230) |

- GraphSAGE 保持第一 (但优势从 +0.14 缩至 +0.05~+0.08); kNN 与 pca_ridge 的相对顺序在 strict split 下翻转 (kNN 2→3)。
- Spearman(random, patient)=1.0 (3 模型, 信息量有限) → 排名稳定性分析需更多模型 (Phase 9, Priority 6 后)。

## 6. 与论文叙事的关系

- H1 ✅ (两数据集); H2 ✅ (两数据集同向); H3 ✅ (DLPFC GraphSAGE/kNN 渠道 + Andersson 无渠道); H4 ✅ (DLPFC); 
- **新增 H6 (双渠道)**: random split 膨胀同时含空间渠道与患者/批次渠道 — 不同平台/组织主导渠道不同。
- Phase 7 补: Andersson 距离曲线 (低密度下 hop 语义需调整)、Thrane V0.1 (n=4 patient 作补充证据)。
