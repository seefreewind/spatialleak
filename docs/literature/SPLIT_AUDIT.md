# SPLIT_AUDIT.md — 文献 split protocol 审计

> 更新: 2026-08-07 · 审计对象: 6 篇空间组学/跨组学预测论文 (≥3–5 篇要求)。
> 依据: 期刊全文 (PMC/PubMed)、作者 reporting summary、官方代码仓库 (均实测可达)。methods 原文不可获取处标注 UNVERIFIED 并以官方代码重构。

## 核心表格

| Method | 期刊/年份 | Dataset | Original split | Patient separated? | Slide separated? | Spatially separated? | Leakage risk |
|--------|-----------|---------|----------------|--------------------|------------------|----------------------|--------------|
| **MultiVI** (Ashuach 2023) | Nat Methods 2023 | PBMC 10x Multiome; DOGMA-seq | **random cell 90/10**; 75% 模态遮蔽 imputation benchmark | ❌ 无 | ❌ 无 | ❌ 无 | **MEDIUM** — in-domain 遮蔽可利用同批次信息；论文自承认跨批次不成立 |
| **NicheTrans** (Wang 2026) | Nat Methods 2026;23:1528–1539 | SMA 小鼠脑; AD STARmap PLUS; Xenium 乳腺癌; MISAR-seq | slide-level (SMA: train 2 slides/test 1, **同 donor**); **Xenium: 单切片内 x-midline 切分**; MISAR: held-out 发育阶段 | ❌ (SMA 同 donor) | ✅ 多数实验 | ⚠️ Xenium 实验中邻近 spot 跨 train/test 边界 | **MEDIUM** |
| **HisToGene** (Pang 2021) | bioRxiv (未正式发表) | HER2+ ST (32 sections); cSCC GSE144240 | **section-level 5-fold**; cSCC: P2 患者 rep2 在 test, rep1/rep3 在 train | ❌ 同一患者跨 train/test | ✅ | ✅ (不同切片) | **MEDIUM** — 个体级混杂跨划分 |
| **ST-Net** (He 2020) | Nat Biomed Eng 2020;4:827 | 23 乳腺癌患者 ST | **leave-one-patient-out CV** | ✅ 完全 | ✅ | ✅ | **LOW (规范对照)** |
| **BABEL** (Wu 2021) | PNAS 2021;118:e2023070118 | Multiome/SNARE-seq/SHARE-seq | **Leiden cluster-based split** (val/test cluster 轮换); GM12878 全程排除训练 | N/A (细胞系) | N/A | N/A | **LOW (规范对照)** — 明确 anti-memorization 动机 + 跨协议外部验证 |
| **SpaGE** (Abdelaal 2020) | Nucleic Acids Res 2020;48:e107 | STARmap/osmFISH/MERFISH/seqFISH+ | **leave-one-gene-out CV**; 变体排除 top-100 相关基因 | N/A (小鼠脑) | N/A | N/A (坐标仅评估用) | **LOW** |

## 逐篇要点

### MultiVI (2023) — 随机 cell split 的代表性实例
- methods 原文: *"As in previous models, we trained on 90% the data and used 10% as a validation set."*
- imputation benchmark: 同一实验内随机遮蔽 75% 细胞的模态 → **无 donor/batch/技术隔离**
- 论文自身方法学反思 (引自原文): *"Our benchmark analyses in Fig. 2 rely on artificially unpaired data, where our model benefits from all data fundamentally being generated in a single batch and by a single technology. This does not reflect real-world situations..."* — 该句正是本项目 H1 的文献内证。
- cross-condition DOGMA-seq 实验是真正的 out-of-sample 测试，但非主 benchmark。

### NicheTrans (2026) — 最新方法的混合实践
- 多数实验做到了 slide-level 划分，值得肯定；但: (a) SMA 数据集 train/test 同 donor; (b) Xenium 实验在**单个切片内部**按 x 坐标中线划分 train/test，空间上相邻 spot 分属两侧，且模型输入含 niche (邻域) 特征 → 边界泄漏渠道。
- 官方代码 `data_manager_breast_cancer.py` 中 `x <= centra` / `x >= centra` 的非严格边界使边界 spot 可能同时进入两侧。

### HisToGene (2021) — section-level 但不保证个体隔离
- 官方代码 `dataset.py`: HER2+ 数据 32 切片 5-fold (fold=5)，test = 1 切片；cSCC 中 P2 患者 rep2 切片测试、rep1/rep3 训练 → **同一患者跨划分**。
- 模型使用坐标嵌入 + 多 spot attention (跨 spot 信息共享)。
- 注意: 该论文未正式发表 (bioRxiv 2021)；methods 原文本次未取到 (网络阻断)，protocol 来自官方代码。

### ST-Net (2020) — 规范实践 (patient-LOO)
- reporting summary (MOESM2): *"We used leave-one-patient-out cross validation. The algorithm was trained on 22 patients and tested on the hold-out patient."*
- 代码 `bin/cross_validate.py` 完全对应 (`--testpatients` 指定留出患者)。
- 外部验证: 10x 数据零修改迁移 + TCGA 批量数据。
- 结论: 2020 年即有高影响力方法采用严格患者隔离 — 说明"随机 spot split"并非技术必然，而是**评估规范缺失**。

### BABEL (2021) — cluster-based split + 外部 holdout
- methods 原文: *"Splitting by cluster reduces similarity between train and test data... Performance on the test cluster is thus a stronger indicator for how well the model will generalize."*
- GM12878 完全排除训练 (最严苛泛化测试)；SNARE-seq/SHARE-seq 跨协议验证；BCC 7 患者零微调应用。
- 结论: RNA↔ATAC 任务存在可复现的严格评估范例，SpatialLeak 的 RNA↔ATAC 场景可参照。

### SpaGE (2020) — 基因级 CV
- leave-one-gene-out 保证目标基因从未进入对齐/预测管线 → 基因泄漏控制良好；但细胞/spot 层面无个体隔离 (小鼠脑多数据混合)。
- 坐标仅用于评估 (Moran's I)，不参与预测 → 无空间信息泄漏渠道。

## 交叉发现

1. **随机 spot/cell split 仍活跃于高影响力方法**: MultiVI (2023) random cell 90/10 是直接例证；NicheTrans (2026) 的 Xenium 单切片 midline split 是"空间划分但无缓冲/无邻域隔离"的变体。
2. **"切片级"不等于"患者级"**: HisToGene 反例证明 section-level split 可能允许同一患者跨 train/test。
3. **规范实践存在且可行**: ST-Net (patient-LOO) 与 BABEL (cluster + 外部 holdout) 未损害其发表价值 — 可作论文叙事中的"评估规范可行性"证据。
4. **泄漏渠道分三层**: (a) 同 spot 级技术/批次效应 (MultiVI in-domain); (b) 同患者不同切片 (HisToGene); (c) 单切片内空间邻域 (NicheTrans Xenium, 无 buffer)。
5. **未见系统性、多数据集、多模型的 leakage-resistant 横向 benchmark** — 正是 SpatialLeak 的定位。

## 局限与 UNVERIFIED

- HisToGene / NicheTrans 的论文 methods 原文本次网络无法获取 (Cloudflare 1015) → split 协议以官方代码重构，标注 UNVERIFIED (manuscript-level)。
- ST-Net methods 付费墙 → 以出版方 reporting summary + 代码双重确认。
- 未覆盖 GLUE/SpatialGlue/GraphST/Cell2location 的评估协议 → Phase 1 扩展审计清单 (见 NEXT_ACTIONS)。
