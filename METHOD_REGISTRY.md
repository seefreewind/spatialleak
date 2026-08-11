# METHOD_REGISTRY.md — 候选方法登记表

> 更新: 2026-08-07 · 审计依据: 公开文献全文 (PMC/PubMed) + 官方代码仓库 (全部 GitHub URL 已于 2026-08-07 实测 HTTP 200)。
> 标注规则: `✅` = 已核实；`UNVERIFIED` = 未能核实，需检索；`N/A` = 不适用。

## 快速总览

| # | 方法 | 年份 | 期刊 | 任务 | 空间坐标 | 邻域/图 | 监督 | 原论文 split 方式 | 泄漏风险 | 纳入 SpatialLeak |
|---|------|------|------|------|---------|---------|------|-------------------|---------|------------------|
| 1 | NicheTrans | 2026 | Nat Methods | 跨组学翻译 (RNA→蛋白/MSI; ATAC↔RNA) | ✅ | ✅ niche graph | ✅ | slide-level (同 donor)；Xenium 单切片内 midline split | MEDIUM | ✅ Phase 2 |
| 2 | SpaGE | 2020 | Nucleic Acids Res | 空间基因 imputation (scRNA 参考) | 仅评估 | ❌ | ❌ | leave-one-gene-out CV | LOW | ✅ (非空间强基线) |
| 3 | Tangram | 2021 | Nat Methods | scRNA→空间 mapping + imputation | ✅ | 可选 | ❌ | N/A (无监督映射) | LOW–MEDIUM | ✅ Phase 2 |
| 4 | gimVI | 2019 | ICML-WS preprint (UNVERIFIED 正式发表) | 空间基因 imputation (paired/unpaired) | ❌ | ❌ | ❌ | N/A | LOW | ✅ (scvi-tools) |
| 5 | MultiVI | 2023 | Nat Methods | 多模态整合 + 跨模态 imputation (RNA/ATAC/蛋白) | ❌ | ❌ | 自监督 | **random cell 90/10** | **MEDIUM** | ✅ Phase 2 (RNA↔ATAC) |
| 6 | GLUE | 2022 | Nat Biotechnol | 多组学整合 (RNA+ATAC+甲基化) | ❌ | ❌ | 半监督 | UNVERIFIED | 待审计 | ⚠️ Phase 2 |
| 7 | scGLUE | 2022 | Bioinformatics (UNVERIFIED 卷期) | scRNA 多组学整合 | ❌ | ❌ | 半监督 | UNVERIFIED | 待审计 | ⚠️ |
| 8 | Seurat WNN | 2021 | Cell | 多模态整合/参考 mapping | ❌ | ❌ | ❌ | N/A | N/A | ⚠️ (非预测) |
| 9 | totalVI | 2021 | Nat Biotechnol | CITE-seq 蛋白降噪/imputation | ❌ | ❌ | 自监督 | N/A | LOW–MEDIUM | ⚠️ Phase 2 (蛋白任务) |
| 10 | SpatialGlue | 2024 | Nat Methods | 空间多组学整合 (RNA+蛋白) | ✅ | ✅ 图注意力 | 自监督 | UNVERIFIED | 待审计 | ⚠️ Phase 2 |
| 11 | ST-Net | 2020 | Nat Biomed Eng | H&E → 基因表达 | ❌ | ❌ | ✅ | **leave-one-patient-out CV** | **LOW (规范对照)** | ⚠️ (非本基准任务) |
| 12 | HisToGene | 2021 | bioRxiv (未正式发表) | H&E → 基因表达 (ViT) | ✅ | ✅ 邻域 attention | ✅ | **section-level；同 patient 跨 train/test** | **MEDIUM** | ⚠️ (非本基准任务) |
| 13 | BABEL | 2021 | PNAS | RNA↔ATAC 翻译 | ❌ | ❌ | ✅ | **cluster-based split + 外部 cell line holdout** | **LOW (规范对照)** | ✅ Phase 2 (RNA↔ATAC) |
| 14 | GraphST | 2023 | Nat Commun | 空间聚类/deconvolution | ✅ | ✅ GNN 对比学习 | 自监督 | UNVERIFIED | 待审计 | ⚠️ |
| 15 | Cell2location | 2022 | Nat Biotechnol | 空间 deconvolution | ✅ | ✅ 邻域正则 | ❌ (贝叶斯) | N/A | N/A | ⚠️ (deconvolution) |

---

## 明细

### 1. NicheTrans (Wang et al.)
- 论文: Wang Z, Zou Q, Lin S, et al. *Nat Methods* 2026;23(8):1528–1539. DOI: 10.1038/s41592-026-03153-3 (preprint bioRxiv 10.1101/2024.12.05.626986)
- 任务: spatial-aware 跨组学翻译 (RNA→蛋白/metabolite, ATAC↔RNA)；Transformer + 空间 niche 特征
- 输入/输出模态: spot 表达 + niche (邻域) 特征 → 目标模态表达
- 空间坐标 ✅ / 邻域 ✅ (spatial kNN/radius graph) / 图结构 ✅ / 监督 ✅
- 原论文 split (从官方代码重构，methods 原文 UNVERIFIED): SMA 数据 slide-level (train V11L12-109_B1/C1, test A1，**同 donor**)；AD 小鼠 train=疾病 rep1, test=疾病 rep2, val=WT；**Xenium 乳腺癌: 单切片内按 x 坐标中线切分 (边界 spot 因非严格不等号可能同时出现在两侧)**；MISAR-seq: held-out 发育阶段
- patient-level split: ❌ (SMA 同 donor) / slide-level: ✅ (多数实验) / external validation: ✅ (WT 对照、跨组织)
- 代码: https://github.com/YSTLab/NicheTrans ✅ | license/checkpoint: UNVERIFIED | GPU: ✅ (高)
- 纳入: ✅ 本 benchmark 的核心复杂模型之一 (Phase 2, 需 GPU 或权重冻结)

### 2. SpaGE (Abdelaal et al.)
- 论文: Abdelaal T, Mourragui S, Mahfouz A, Reinders MJT. *Nucleic Acids Res* 2020;48(18):e107. DOI: 10.1093/nar/gkaa740
- 任务: 用 scRNA-seq 参考 impute 空间转录组中未测基因 (PRECISE 域适应 + kNN)
- 空间坐标: 仅用于评估 (Moran's I) / 无监督
- 原 split: leave-one-gene-out CV；STARmap 变体排除与目标基因 top-100 相关基因
- external: Allen Brain Atlas ISH 验证 ✅
- 代码: https://github.com/tabdelaal/SpaGE ✅ (MIT) | GPU: ❌ (CPU)
- 纳入: ✅ 作为强非空间基线/方法学对照

### 3. Tangram (Singhal et al.)
- 论文: Singhal V, Chou N, Lee J, et al. *Nat Methods* 2021;18:588–597. DOI: 10.1038/s41592-021-01129-9
- 任务: 将 scRNA-seq 细胞映射到空间位点；可反推基因 imputation
- 空间坐标 ✅ | 无监督优化 (可加 scRNA 先验) | split: N/A (mapping) — 作为预测任务评测时的 split 方式 UNVERIFIED
- 代码: https://github.com/broadinstitute/Tangram ✅ | license/checkpoint: UNVERIFIED | GPU: 可选
- 纳入: ✅ Phase 2 (gene imputation 任务)

### 4. gimVI (Lopez et al.)
- 论文: Lopez R, Nazaret A, Langevin M, et al. "A joint model of unpaired data from scRNA-seq and spatial transcriptomics for imputing missing gene expression measurements." ICML 2019 Computational Biology Workshop. **正式期刊发表状态 UNVERIFIED**
- 任务: 空间基因 imputation (联合 VAE, 支持 paired/unpaired)
- 代码: scvi-tools 内置 ✅ (https://github.com/scverse/scvi-tools ✅) | GPU: 可选
- 纳入: ✅ Phase 2 (imputation 任务)

### 5. MultiVI (Ashuach et al.)
- 论文: Ashuach T, et al. *Nat Methods* 2023;20(8):1222–1231. DOI: 10.1038/s41592-023-01909-9
- 任务: 多模态 VAE 整合 RNA+ATAC(+蛋白)，缺失模态 imputation
- 原 split (methods 原文核实): **"we trained on 90% the data and used 10% as a validation set" — random cell-level 90/10**；imputation benchmark 随机遮蔽 75% 细胞的某一模态；cross-condition (stimulated PBMC) 无重训外部测试
- patient/donor split: ❌ | slide split: ❌ | external: 部分 (cross-condition)
- 泄漏风险: **MEDIUM** — in-domain imputation benchmark 可依赖同批次信息；论文自身承认 "does not reflect real-world situations" (不同批次/技术)
- 代码: scvi-tools ✅ | GPU: ✅
- 纳入: ✅ Phase 2 (RNA↔ATAC 任务) — **本文档档最重要的"随机 cell split 高影响力实例"**

### 6. GLUE (Cao & Gao)
- 论文: Cao ZJ, Gao G. *Nat Biotechnol* 2022;40:1458–1466. DOI: 10.1038/s41587-022-01284-4 (卷期/DOI UNVERIFIED，以检索为准)
- 任务: 多组学整合 (RNA+ATAC+甲基化)，图链接嵌入
- 代码: https://github.com/gao-lab/GLUE ✅ | 原论文 split: UNVERIFIED | GPU: ✅
- 纳入: ⚠️ Phase 2 (RNA↔ATAC)，先审计其评估协议

### 7. scGLUE (Cao & Gao)
- 论文: Cao ZJ, Gao G. *Bioinformatics* 2022. 卷期/DOI UNVERIFIED
- scRNA-seq 版图链接整合；官方仓库未检索到 (GitHub 搜索无结果，UNVERIFIED)
- 纳入: ⚠️ 优先级低

### 8. Seurat WNN (Hao et al.)
- 论文: Hao Y, et al. *Cell* 2021;184:3573–3587. DOI: 10.1016/j.cell.2021.04.048
- 任务: 多模态加权近邻整合/参考 mapping (RNA+蛋白/ATAC)
- 无监督、非预测模型 → 纳入 ⚠️ (仅作为方法学参照)

### 9. totalVI (Gayoso et al.)
- 论文: Gayoso A, et al. *Nat Biotechnol* 2021;39:1278–1287 (卷页 UNVERIFIED，以检索为准). DOI: 10.1038/s41587-021-00901-0 (UNVERIFIED)
- 任务: CITE-seq 蛋白表达降噪/imputation
- 代码: scvi-tools ✅ | 原 split: N/A (自监督降噪)
- 纳入: ⚠️ Phase 2 (如选蛋白任务)

### 10. SpatialGlue (Long et al.)
- 论文: Long Y, et al. *Nat Methods* 2024;21:1322–1332 (卷页 UNVERIFIED). DOI: 10.1038/s41592-024-02311-9 (UNVERIFIED)
- 任务: 空间多组学整合聚类 (RNA+蛋白共测 Visium)，图注意力
- 基准数据: tonsil + lymph node, 2 donors, 4 切片 (GSE263617 ✅)
- 代码: https://github.com/JinmiaoChenLab/SpatialGlue ✅ | 原 split: UNVERIFIED | GPU: ✅
- 纳入: ⚠️ Phase 2 (多组学任务)；其基准数据 GSE263617 已是本项目的蛋白任务候选

### 11. ST-Net (He et al.)
- 论文: He B, et al. *Nat Biomed Eng* 2020;4:827–834. DOI: 10.1038/s41551-020-0578-x
- 任务: H&E patch → 基因表达 (DenseNet-121)
- 原 split (reporting summary + 代码核实): **leave-one-patient-out CV** (23 patients)；external: 10x 数据无修改迁移 + TCGA
- 泄漏风险: **LOW** — 本项目规范实践对照
- 代码: https://github.com/bryanhe/ST-Net ✅ | GPU: ✅
- 纳入: ⚠️ 任务不同 (histology→RNA)，但作为"高影响力论文如何做 patient split"的引用样例

### 12. HisToGene (Pang et al.)
- 论文: Pang M, Su K, Li M. *bioRxiv* 2021. DOI: 10.1101/2021.11.28.470212 (**未正式发表**，UNVERIFIED 于 2026-08-07)
- 任务: H&E + 坐标 → 基因表达 (ViT)，超分辨率预测
- 原 split (官方代码核实，methods 原文 UNVERIFIED): **section-level split；HER2+ ST 数据留一切片；cSCC 数据 P2 患者一个切片在 test、其余在 train → 同 patient 跨 train/test**
- 泄漏风险: **MEDIUM** (同一患者不同切片共享个体/技术混杂)
- 代码: https://github.com/maxpmx/HisToGene ✅ (MIT)
- 纳入: ⚠️ 任务不同；引用为"section-level 但不保证 patient 隔离"实例

### 13. BABEL (Wu et al.)
- 论文: Wu KE, Yost KE, Chang HY, Zou J. *PNAS* 2021;118(15):e2023070118. DOI: 10.1073/pnas.2023070118
- 任务: 单细胞 RNA↔ATAC 双向翻译 (VAE + adversarial)
- 原 split (methods 原文核实): **Leiden 聚类保留 cluster 作 val/test，5-fold 轮换；GM12878 细胞系完全排除在训练外作为最难泛化测试；cross-protocol 外部验证 (SNARE-seq/SHARE-seq)；BCC 患者数据零微调应用**
- 泄漏风险: **LOW** — 规范实践对照 (明确 anti-memorization 动机)
- 代码: https://github.com/wukevin/babel ✅ | GPU: ✅
- 纳入: ✅ Phase 2 (RNA↔ATAC 任务)

### 14. GraphST (Long et al.)
- 论文: Long Y, et al. *Nat Commun* 2023. DOI UNVERIFIED
- 任务: 空间聚类 + deconvolution (GNN 对比学习)
- 代码: https://github.com/JinmiaoChenLab/GraphST ✅ | 原 split: UNVERIFIED | GPU: ✅
- 纳入: ⚠️ (聚类任务非预测主场景；可作空间模型参照)

### 15. Cell2location (Kleshchevnikov et al.)
- 论文: Kleshchevnikov V, et al. *Nat Biotechnol* 2022;40:661–671 (卷页 UNVERIFIED). DOI: 10.1038/s41587-021-01139-4 (UNVERIFIED)
- 任务: scRNA 参考 → 空间 cell type deconvolution (贝叶斯, 邻域正则)
- 代码: https://github.com/BayraktarLab/cell2location ✅ | GPU: ✅
- 纳入: ⚠️ (deconvolution 任务，如选作第五类任务)

---

## 审计结论

1. **存在明确的评估缺口**：即使 2022–2026 高影响力方法 (MultiVI 2023、NicheTrans 2026、HisToGene 2021) 仍使用 random cell split 或"切片级但不保证个体隔离"的划分。
2. **存在规范实践对照**：ST-Net (patient-LOO)、BABEL (cluster-split + 外部 holdout) 证明严格划分可行且不必然损害报告。
3. **本 benchmark 的任务版图**：空间基因 imputation (SpaGE/Tangram/gimVI) + RNA↔ATAC (MultiVI/GLUE/BABEL) + RNA→蛋白 (NicheTrans/totalVI/SpatialGlue) + (可选) histology→RNA (ST-Net/HisToGene)。**Pilot 阶段只做基因表达预测任务，其余任务 Phase 2 扩展。**
4. 未核实项: GLUE/scGLUE/SpatialGlue/GraphST 原论文 split 方式、gimVI 发表状态、totalVI 卷页 → 全部标注 UNVERIFIED，Phase 1 扩展审计。
