# PHASE0_1_REPORT.md — Phase 0–1 状态报告

> 日期: 2026-08-07 · 阶段: 项目初始化 + 文献/数据审计完成 · 状态: **Pilot 可启动 (GO 条件满足)**

---

## 1. 项目可行性评估

**可行，且条件优于预期。**
- 环境: Mac M5 / 17 GB RAM / CPU-only；scanpy 1.10.3 + anndata + sklearn + torch 2.8.0 已装 (系统 Python 3.9.6)；squidpy 待装 (可选)。
- 数据: Pilot 数据 (DLPFC 12 切片, 3 donors, 47,681 spots) 下载链路已逐 URL 实测 (AWS S3 + GitHub raw, ~160 MB, 无注册无伦理限制)。
- 计算: Pilot 全部模型 CPU 可跑 (数分钟级)；无需 GPU。
- 文献: 6 篇论文 split protocol 完成审计，评估缺口明确存在 (见 §3)。

## 2. 最强科学假设 (按证据强度排序)

1. **H1 (随机 split 高估性能)** — 证据: MultiVI (Nat Methods 2023) 明确采用 random cell 90/10 且论文自承认 in-domain benchmark 不反映跨批次现实；这是直接文献内证。**最强假设。**
2. **H2 (自相关→膨胀)** — DLPFC 层状结构 Moran's I 极高，机制清晰，Pilot 即可检验。
3. **H3 (spatial-aware 优势来自邻域共享)** — NicheTrans Xenium 单切片 midline split 提供现成反例素材；spatial kNN baseline 直接检验。
4. **H4 (严格划分下差距缩小)** — 与 H1 同源，Pilot 主比较。
5. **H5 (LSS 稳定性)** — 依赖 Phase 4–6 完成后定义。

## 3. 文献中的评估缺口

- **随机 spot/cell split 仍活跃**: MultiVI (2023) random cell 90/10; NicheTrans (2026) 单切片内 midline split 无缓冲; HisToGene (2021) section-level 但同患者跨 train/test。
- **规范实践存在**: ST-Net (2020) leave-one-patient-out; BABEL (2021) cluster-split + GM12878 全程 holdout + 跨协议验证 → 严格评估可行，非技术必然。
- **缺口**: 尚无系统、多数据集、多模型、统一严格划分的横向 leakage-resistant benchmark → SpatialLeak 定位成立。

## 4. 最合适的数据

| 用途 | 数据集 | 理由 |
|------|--------|------|
| **Pilot (选定)** | D1 DLPFC (3 donors/12 slides/47,681 spots) | 同时覆盖 random/spatial-block/slide/patient 四级划分; 层标注现成; 下载链路已核验; 无伦理门槛 |
| Patient 主场景 | D2 Andersson HER2+ (8 patients/36 sections) | 8 患者，patient-held-out 金标准 |
| Within-slide 扩展 | D3 10x 乳腺癌 v1.1.0 (2 sections) | 肿瘤组织、密集 spot |
| 外部验证 (脑) | D7 spatialDLPFC (10 donors/30 blocks) | 同组织独立研究 (途径待核验) |
| 蛋白任务 | D8 GSE213264 / D9 GSE263617 / D11 | RNA+蛋白配对空间模态 |

## 5. Pilot 设计 (已锁定 ANALYSIS_LOCK.md §1)

- **数据集**: DLPFC 12 切片全量 (HVG-2000 特征; 目标 = Moran's I top-50 基因)
- **任务**: 多基因表达预测 (per-gene Pearson/Spearman/RMSE, 聚合 + per-feature 保留)
- **Splits**: ① Random 80/10/10 ② Spatial block (per-slide 2×2 grid, buffer 0 / 2 array-step) ③ Patient-held-out (LOO donor)
- **Models**: Mean · PCA+Ridge · Spatial kNN (k=15) · GraphSAGE (可选, CPU)
- **Repetition**: 5 seeds (0–4), 全局 seed 42
- **统计**: slide-level bootstrap (pilot 200), CI + BH-FDR
- **GO 标准 (满足任一)**: A) random vs block 明显下降; B) 模型排名改变; C) 复杂模型优势缩小; D) 自相关-膨胀相关。**全无差异 → 分析原因换任务/数据，不改数据与指标。**

## 6. 最大风险

| 风险 | 概率 | 缓解 |
|------|------|------|
| 3-donor patient-held-out 功效不足 | 中 | slide-level bootstrap (n=12)、承认限制、Phase 14 引入 D2 (8 patients) |
| donor 间库大小/技术混杂被误读为"泄漏" | 中 | 已含 Mean baseline + Phase 10 matched analysis 区分 leakage vs domain shift |
| Moran's I top-50 基因选择机制争议 | 低 | 全数据属性选择, 文档化; 补充 permuted-coordinate 检验 (Phase 13) |
| Andersson zip 密码 / spatialDLPFC 途径受阻 | 中 | Backup 清单完整 (D3/D4/D5/D6/D9/D12) |
| 外部网络不稳定 (bioRxiv Cloudflare 等) | 中 | 代码重构 + UNVERIFIED 标注, 已记录 |

## 7. 资源估算

| 项 | 估算 |
|----|------|
| 下载 | ~160 MB (DLPFC filtered h5 ×12 + 坐标 + 层标注; 跳过 6.4 GB TIF) |
| 磁盘 (预处理缓存) | ~1 GB (HVG 子集 h5ad) |
| RAM | < 8 GB (逐切片处理 + HVG 子集后拼接) |
| VRAM | 0 (CPU-only) |
| Runtime (Pilot) | Mean/PCA+Ridge/Spatial kNN: 数分钟; GraphSAGE: ~10–20 min CPU (5 seeds) |
| 全规模 Phase 2 模型 (NicheTrans 等) | 需 GPU → 优先官方 pretrained/frozen embeddings, 不重训 foundation model |

## 8. 下一步具体命令

```bash
# 1) 安装补充依赖 (squidpy 可选, 非阻塞)
pip install -r requirements.txt

# 2) 下载 DLPFC (~160 MB)
python spatialleak/scripts/download_dlpfc.py --out spatialleak/data/raw/dlpfc

# 3) 预处理 → 缓存 h5ad
python spatialleak/scripts/preprocess_dlpfc.py --config spatialleak/configs/datasets/dlpfc.yaml

# 4) 单元测试 (splits/metrics)
python -m pytest spatialleak/tests -q

# 5) Pilot benchmark (3 splits × 4 models × 5 seeds, CPU)
python spatialleak/scripts/pilot_benchmark.py --config spatialleak/configs/experiments/pilot_dlpfc.yaml

# 6) 复核 Pilot GO 标准 (§5) 并在 PROJECT_STATUS.md 记录结论
```

## 9. Hypothesis challenged 记录

- **挑战**: 假设"所有空间组学预测论文均采用随机 split" — **不成立**。ST-Net 与 BABEL 已实现严格划分。→ 论文叙事改为"缺口存在但不普遍，需系统性量化" (H1 仍成立: 采用随机 split 的论文占比与膨胀幅度需量化)。
- **挑战**: 假设 SpaGE 可作"空间模型"纳入 — 实际其坐标仅用于评估。→ 归入非空间强基线类别。
- **挑战**: HisToGene 原以为 Nature Communications 发表 — 实际仅 bioRxiv (2026-08-07 检索时未正式发表)。→ METHOD_REGISTRY/SPLIT_AUDIT 已如实更正。
