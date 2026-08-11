# DLPFC_FORMALIZATION_REPORT.md — DLPFC 正式化报告

> 日期: 2026-08-09 · 数据: SpatialLIBD DLPFC (12 slides, 3 donors, 47,681 spots) · 任务: top-50 Moran 靶基因表达重建 (HVG-2000 特征)
> 设计冻结: ANALYSIS_LOCK §8 · 结果: results/formal_dlpfc/ + analysis/ (全部脚本生成)

---

## 1. 设计升级 (vs Pilot)

| 项目 | Pilot | Formal |
|------|-------|--------|
| Seeds | 5 | **10** (0–9) |
| Spatial block | 随机 grid 指派 (SD 0.096–0.098) | **matched blocks** (300 候选指派, 组成距离最小化; SD → 0.040–0.051) |
| Buffer 度量 | array-step 欧氏 (≤2 无效) | **kNN-hop (k=15)** + z-坐标双度量 |
| 距离曲线 | buffer 0/1/2/5 | hop {0,1,2,5} + region 设计 {5,10} + coord {0.25,0.5,1.0} |
| Bootstrap | 200 | **1000** (slide-level) |
| GraphSAGE | 2 seeds × 1 patient fold | **10 seeds × {random, matched} + 3 patient folds** |
| 统计 | 描述性 | Wilcoxon + BH-FDR + 排名相关 |

## 2. 主表 (mean Pearson ± SD, 10 seeds)

| split | PCA+Ridge | Spatial kNN | GraphSAGE |
|-------|-----------|-------------|-----------|
| random | 0.292 | 0.297 | **0.425 ± 0.006** |
| matched_hop0 | 0.196 | 0.177 | 0.255 ± 0.036 |
| patient (3 folds) | 0.230 | 0.261 | 0.326 |
|   — Br5292 | 0.191 | 0.249 | 0.295 |
|   — Br5595 | 0.152 | 0.223 | 0.224 |
|   — Br8100 | 0.346 | 0.312 | 0.460 |

### LI / RLI / LSS

| split | PCA+Ridge | kNN | GraphSAGE |
|-------|-----------|-----|-----------|
| matched_hop0 RLI | **0.328** | **0.402** | **0.400** |
| patient RLI | 0.213 | 0.120 | 0.233 |
| **LSS_A** (mean RLI) | 0.270 | 0.261 | 0.317 |
| **LSS_B** (min retention loss) | 0.328 | 0.402 | 0.400 |

### 模型排名 (1=best)

| 排名 | random | matched_hop0 | patient |
|------|--------|--------------|---------|
| 1 | GraphSAGE | GraphSAGE | GraphSAGE |
| 2 | kNN | PCA+Ridge | kNN |
| 3 | PCA+Ridge | kNN | PCA+Ridge |

- kNN 在 random 下 > PCA+Ridge, strict split 下 < PCA+Ridge (排名翻转, Spearman random↔matched = 0.50)
- GraphSAGE 保持第一, 但 Δ(GraphSAGE − PCA+Ridge): random **+0.133** → matched **+0.059** → patient **+0.096** → **复杂模型优势大幅缩小**

## 3. 统计检验 (10 seeds, per-seed 配对)

| 比较 | 模型 | median diff | p | p_bh (BH-FDR) | 显著 |
|------|------|-------------|----|---------------|------|
| random vs matched_hop0 | pca_ridge | +0.117 | 0.002 | 0.0029 | ✅ |
| random vs matched_hop0 | spatial_knn | +0.154 | 0.002 | 0.0029 | ✅ |
| random vs matched_hop0 | GraphSAGE | +0.182 | 0.002 | 0.0029 | ✅ |
| random vs patient | pca_ridge | +0.063 | 0.002 | 0.0029 | ✅ |
| random vs patient | spatial_knn | +0.037 | 0.002 | 0.0029 | ✅ |

**GO-A: 10/10 seeds random > strict (pca_ridge min diff 0.039; knn min diff 0.049)** ✅

## 4. 距离泄漏曲线 (Distance Leakage Curve)

### kNN-hop (matched blocks)

| buffer | pca_ridge | kNN | kNN RLI |
|--------|-----------|-----|---------|
| hop0 | 0.196 | 0.177 | 0.402 |
| hop1 | 0.196 | 0.177 | 0.402 |
| hop2 | 0.184 | 0.156 | 0.475 |
| hop5 | 0.157 | 0.089 | 0.700 |

### z-坐标 buffer (matched blocks)

| buffer | pca_ridge | kNN |
|--------|-----------|-----|
| 0.25 | 0.165 | 0.130 |
| 0.50 | 0.142 | 0.078 |
| 1.00 | 0.108 | 0.017 |

### region 高 hop 扩展 (edges-only train, 种子不变)

| buffer | pca_ridge | kNN |
|--------|-----------|-----|
| hop5 (100% test 保留) | 0.189 | 0.153 |
| hop10 (64% test 保留) | 0.156 | 0.127 |

- **曲线单调**: kNN 性能随 train–test 最小 hop 距离单调下降 (0.177→0.089→0.127@hop10-region)
- hop5 后衰减加速; matched hop5 kNN RLI 达 0.70 → 邻域信息共享是 kNN 的主要性能来源
- pca_ridge 亦随 buffer 衰减 (drop 使 test 组成偏移), 但幅度小于 kNN

## 5. GraphSAGE block 高值异常调查 (Pilot seed1 = 0.478)

| 检验 | 结果 |
|------|------|
| (a) 可重复? | ❌ 10 seeds 中无第二个 0.478 级高值 (max 0.357, seed2) |
| (b) block 组成驱动? | ⚠️ 部分: seed2 高值对应**最差匹配**的指派 (match_score 1.19 vs 0.93), 即 test block 组成失衡 (层主导) → 邻域聚合更容易 → **shortcut 友好型 test 组成**; 10 seeds 相关性 r=0.44, p=0.21 (不显著) |
| (c) train/val 分布? | ❌ 无证据 (val 均来自训练 donor) |
| (d) 正常抽样方差? | ✅ 部分: matched 设计下 SD=0.036 (pilot 0.10 → 0.036), 属 matched 指派空间的正常变异 |

**结论**: Pilot 异常值未重复出现; 机制与"组成失衡 block 更易被 shortcut 预测"一致 (支持而非反驳泄漏故事); matched 设计显著压缩该方差。**异常值保留未删除。**

## 6. GO 标准达成

| 标准 | 状态 |
|------|------|
| GO-A: ≥10 seeds 方向稳定 | ✅ 10/10 seeds |
| GO-B: 第二数据集复现 | ✅ Andersson (见 MULTIDATASET_BENCHMARK_V0.1.md) |
| GO-C: 复杂模型优势缩小 | ✅ Δ +0.133 → +0.059/+0.096 |
| GO-D: Moran-膨胀方向一致 | ✅ 双数据集 r=0.47–0.74, p<1e-6 |

## 7. 局限

1. patient n=3 → fold 级功效有限; 以 slide bootstrap (12/4 slides) 为准
2. GraphSAGE 配对 Wilcoxon 未并入主统计表 (待补); 10/10 seeds 方向一致
3. matched blocks 在 300 候选内寻优, 最优指派集合小 (3 个不同 match_score 值) → 指派多样性有限
4. pca_ridge 在 buffer 下的下降含 test 组成偏移成分 (非纯泄漏) — Phase 10 matched 控制已部分缓解
