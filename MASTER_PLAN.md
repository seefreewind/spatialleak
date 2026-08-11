# MASTER_PLAN.md — SpatialLeak 主计划

> 维护者: 项目组 · 更新: 2026-08-07 (Phase 0–1 完成)
> 本文件定义每个阶段的 目标/输入/输出/GO-NO-GO标准/依赖/风险。指标锁定见 ANALYSIS_LOCK.md。

## 项目定位

**一个空间组学机器学习方法学 benchmark 与 evaluation framework，而非新预测模型。**
目标结论形式：
> (1) Random spot-level splitting systematically inflates reported performance in spatial omics prediction;
> (2) The apparent superiority of several complex spatial models diminishes under patient-, slide-, and dataset-held-out evaluation.

---

## 阶段总览

| Phase | 名称 | 状态 |
|-------|------|------|
| 0 | 项目初始化 | ✅ DONE |
| 1 | 文献与 Benchmark 审计 | ✅ DONE (初版) |
| 2 | 公共数据集筛选与下载 | 🔜 NEXT |
| 3 | Leakage-resistant split framework | 🔜 NEXT (代码骨架已建) |
| 4 | 泄漏量化指标 (LI / RLI / LSS) | 🔜 NEXT (候选定义已建，Pilot 后冻结) |
| 5 | Baseline 设计 | 🔜 NEXT (代码骨架已建) |
| 6 | 最小 Pilot | 🔜 NEXT |
| 7 | 空间自相关机制分析 | ⏳ 计划 |
| 8 | Distance Leakage Curve | ⏳ 计划 |
| 9 | 模型排名稳定性 | ⏳ 计划 |
| 10 | Matched Null / Shortcut Audit | ⏳ 计划 |
| 11 | 模型复杂度收益 | ⏳ 计划 |
| 12 | 统计分析 | ⏳ 计划 |
| 13 | Negative Controls | ⏳ 计划 |
| 14 | Cross-dataset external validation | ⏳ 计划 |
| 15–16 | 论文 Figure / Table | ⏳ 计划 |
| 17–18 | 叙事与 Reporting guideline (SOEMC) | ⏳ 计划 |
| 19 | 代码质量 | ⏳ 贯穿 |
| 20 | 资源控制 | ⏳ 贯穿 |
| 21 | Research Integrity | ⏳ 贯穿 |

---

## Phase 0 — 项目初始化

- **目标**: 建立可复现项目骨架；检查环境。
- **输入**: 空目录 `/Users/zy/Documents/SpatialLeak：空间组学模型的泄漏安全评测`。
- **输出**: README / MASTER_PLAN / PROJECT_STATUS / DATA_MANIFEST / METHOD_REGISTRY / ANALYSIS_LOCK / environment.yml / requirements.txt / configs / src / scripts / results / docs / manuscript 骨架。
- **GO/NO-GO**: 目录结构完整；Python 核心依赖可用 (scanpy/torch/sklearn) → ✅ GO。
- **依赖**: 无。
- **风险**: 系统 Python 3.9.6 较旧；squidpy 缺失 → 先以 scipy cKDTree 实现邻域，squidpy 仅用于可视化。

## Phase 1 — 文献与 Benchmark 审计

- **目标**: 审计 ≥10 个候选方法 (METHOD_REGISTRY.md)；审计 ≥3–5 篇高水平论文的 split protocol (SPLIT_AUDIT.md)。
- **输入**: 公开文献 (PMC/PubMed/bioRxiv) + 官方代码仓库。
- **输出**: METHOD_REGISTRY.md (15 方法)；docs/literature/SPLIT_AUDIT.md (6 篇论文，全部关键事实已验证)。
- **GO/NO-GO**: 文献中存在随机 spot/cell split 的高影响力实例 (✅ MultiVI 90/10 random cell；NicheTrans 单切片内 midline split；HisToGene section-level 且同 patient 跨 train/test) + 存在规范实践对照 (✅ ST-Net patient-LOO；BABEL cluster-split) → **GAP 明确，GO**。
- **依赖**: 无。
- **风险**: 部分论文 methods 原文不可获取 (HisToGene/NicheTrans bioRxiv 被 Cloudflare 拦截) → 以官方代码重构 split 逻辑，标注 UNVERIFIED。

## Phase 2 — 公共数据集筛选与下载

- **目标**: 下载 Pilot 数据 (DLPFC 12 切片)；核验 DATA_MANIFEST 中其余候选；完成下载状态与质量状态更新。
- **输入**: DATA_MANIFEST.md (12 个候选，URL 已核验)。
- **输出**: data/raw/dlpfc/ (filtered h5 ×12 + tissue_positions + layer map, ~160 MB)；预处理缓存 data/processed/。
- **GO/NO-GO**: 12/12 切片下载完整 + 哈希校验 + 预处理可运行 → GO。
- **依赖**: 网络 (AWS S3 + GitHub raw)；scanpy/anndata。
- **风险**: 磁盘/网络中断 → 脚本支持断点续传与重跑；`UNVERIFIED` 条目 (Andersson 密码保护 zip、spatialDLPFC 下载途径) 待 Phase 2 核验。

## Phase 3 — Leakage-resistant split framework

- **目标**: 实现 5 类 split：Random spot / Spatial block (grid + clustering, buffer 0/1/2/5 邻距) / Slide-held-out / Patient-held-out / Dataset-held-out。
- **输入**: 预处理后 DLPFC h5ad + 坐标。
- **输出**: src/splits/* (代码骨架已建)；split 元数据 JSON (train/val/test spot id、buffer 参数、随机种子)。
- **GO/NO-GO**: 单元测试通过 (不重叠、全覆盖、buffer 距离属性、组级划分完整性) → GO。
- **依赖**: Phase 2。
- **风险**: buffer 在 10x array 坐标与物理距离之间的换算 (array step ≈ 100 µm) 需文档化；单切片 block 数不足时退化处理。

## Phase 4 — 泄漏量化指标

- **目标**: 冻结 LI / RLI / LSS 定义。
- **输入**: Phase 1–3。
- **输出**: ANALYSIS_LOCK.md 更新 (指标冻结)。
- **GO/NO-GO**: 3 个候选 LSS 定义完成冗余性检查，选出 1 个主定义 + 1 个敏感性定义 → GO。
- **依赖**: 指标与 Phase 6 Pilot 数据同批产出。
- **风险**: 指标过度工程化 → 选择原则：最简单、可解释、非重复表达。

## Phase 5 — Baseline 设计

- **目标**: 实现 10 类 baseline：Mean / Median / spatial kNN / expression kNN / PCA+Ridge / ElasticNet / RF / XGBoost(如合理) / MLP / cell-type composition (如有)。
- **输入**: Phase 2 数据。
- **输出**: src/models/* 可运行。
- **GO/NO-GO**: 单元测试 + 极小数据冒烟测试 → GO。
- **依赖**: Phase 2。
- **风险**: XGBoost 未安装 → 标记可选。

## Phase 6 — 最小 Pilot

- **目标**: 1 数据集 (DLPFC) × 1 任务 (多基因表达预测) × 3 splits (random / spatial-block / patient-held-out) × 4 模型 (Mean / PCA+Ridge / Spatial kNN / GraphSAGE-可选)。
- **输入**: Phase 2–5。
- **输出**: results/pilot/*.csv (per-gene、per-seed、per-split) + 运行日志 + config 存档。
- **GO/NO-GO 标准** (满足任一即可 GO；见 PHASE0_1_REPORT §5.6)：
  - A: random vs spatial-block 出现明显性能下降；
  - B: 模型排名在 strict split 下改变；
  - C: 复杂模型优势在 strict split 明显缩小；
  - D: 空间自相关与性能膨胀显著相关。
- **依赖**: Phase 2–5；≥5 seeds。
- **风险**: DLPFC 层状结构导致 Moran's I 极高 → 属预期 (这正是 H2 材料)；3 个 donor 的 patient-held-out 统计功效有限 → slide-level bootstrap + 承认限制。

## Phase 7 — 空间自相关机制分析

- **目标**: Moran's I / Geary's C / NN expression similarity / distance–similarity 曲线 / cell-type 邻域同质性 / library-size 自相关；拟合 LeakageInflation ~ MoranI + Dataset + Model (多数据集时 mixed-effects)。
- **GO/NO-GO**: 完成相关性检验 + 报告效应量与 CI。
- **依赖**: Phase 6 (性能数据)。

## Phase 8 — Distance Leakage Curve

- **目标**: 逐渐增大 train–test 最小空间距离 (0/50/100/250/500/1000 µm 或 NN-hop)，绘制 Spatial Generalization Curve。
- **GO/NO-GO**: 仅当 SG-AUC 提供独立信息时引入，否则仅报告曲线本身 (防指标膨胀)。
- **依赖**: Phase 6。

## Phase 9 — 模型排名稳定性

- **目标**: Rank_random vs Rank_patient vs Rank_external 的 Spearman/Kendall tau；回答 "Are current leaderboards robust to leakage-resistant evaluation?"。

## Phase 10 — Matched Null / Shortcut Audit

- **目标**: 区分 Leakage 与 legitimate domain shift：matched spatial blocks、cell-type 组成匹配、深度/丰度/密度匹配分析。

## Phase 11 — 模型复杂度收益

- **目标**: ΔComplexModel = Complex − StrongSimpleBaseline；比较 random vs strict 下的 Δ。

## Phase 12 — 统计分析

- **目标**: patient/slide-level bootstrap (≥1000, pilot 200)；95% CI；paired comparison；Wilcoxon signed-rank / mixed-effects；BH-FDR。禁止把 spot 当独立单位。

## Phase 13 — Negative Controls

- **目标**: 坐标置换 / 邻域图打乱 / expression-matched 随机邻居 / cell-type 分层随机 / distance-matched train-test。

## Phase 14 — Cross-dataset external validation

- **目标**: ≥2 个独立外部场景；Discovery 2–3 + External ≥2；Tier 1–5 层级清晰 (within-slide → cross-platform)。

## Phase 15–16 — Figures & Tables

- **目标**: Fig1 framework / Fig2 benchmark overview / Fig3 leakage inflation / Fig4 Moran's I 机制 / Fig5 leaderboard instability / Fig6 complex vs simple / Fig7 external (可与 Fig6 合并)；Table 1–5 + 全量 supplement。

## Phase 17–18 — 叙事与 Reporting guideline

- **目标**: Problem → Hidden issue → Consequence → Benchmark → Finding → Mechanism → Recommendation 叙事；提出 SOEMC 最小检查清单 (10 条，见 ANALYSIS_LOCK 附录)。

## Phase 19–21 — 代码质量 / 资源 / 完整性

- 贯穿性要求：configuration-driven、CLI 可复现、logging、固定种子、单元测试、预处理缓存、checkpoint、graceful resume；>2h 或 >16GB VRAM 前先 small pilot；优先 pretrained/frozen embeddings；不训练 foundation model；禁止一切 Phase 21 列出的行为。

---

## 依赖图

```
Phase 0 ──► Phase 1 ──► Phase 2 ──► Phase 3 ──► Phase 4 ──► Phase 6 ──► Phase 7/8/9/10/11 ──► Phase 12 ──► Phase 13/14 ──► Phase 15/16 ──► Phase 17/18
                │           │           │                         ▲
                │           │           └──────────► Phase 5 ──────┘
                └───────────┴──────────────────────────────────────┘ (Pilot 结论回流冻结指标/方法清单)
```

## 全局风险与缓解

| 风险 | 缓解 |
|------|------|
| 3-donor patient-held-out 功效不足 | slide-level bootstrap (12 slides)、承认限制、加入 Andersson 8-patient 数据 (Phase 14) |
| 系统 Python 3.9.6 过旧 | 已兼容现有栈；必要时用 uv 建 3.10 venv (不依赖 conda) |
| 论文原文不可获取 | 以官方代码重构 split 逻辑并标注 UNVERIFIED |
| 外部数据下载受阻 (Andersson zip 密码 / spatialDLPFC Globus) | 备用数据集清单完整 (10x 系 / Thrane / GEO)，可无缝切换 |
| 结论不显著 (All-splits-identical) | 分析原因、换任务/数据，绝不改数据或指标 (见 PHASE0_1_REPORT §6) |
