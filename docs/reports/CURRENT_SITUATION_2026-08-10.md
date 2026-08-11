# SpatialLeak 当前情况交接

> 日期: 2026-08-10  
> 项目目录: `/Users/zy/Documents/SpatialLeak：空间组学模型的泄漏安全评测/spatialleak`  
> 当前阶段: **Phase 0-15D 已完成；manuscript draft package 已就绪；下一步需要用户提供投稿信息**

## 1. 一句话结论

SpatialLeak 已从数据、split 框架、正式多数据集 benchmark、统计刷新、GraphSAGE 整合、图表资产、论文图、到 manuscript draft package 全部推进完成。核心结论稳定：**random spot/cell split 会在空间组学预测中系统性抬高表观泛化性能；这种膨胀来自两个应分开报告的渠道，即 within-section spatial-neighborhood leakage 与 patient/batch shortcut。**

## 2. 项目定位

SpatialLeak 是一个 **leakage-resistant benchmark / evaluation framework**，不是新预测模型论文。

拟定论文方向:

**SpatialLeak: Leakage-resistant benchmarking reveals inflated generalization in spatial omics prediction**

目前推荐路线:

- 不把额外 SOTA 模型纳入主分析。
- SOTA 保留为 Discussion 或 supplementary audit candidate。
- 最终图采用 Python 生成。
- 默认不生成 PDF；后续投稿稿件优先 DOCX 或 LaTeX，取决于目标期刊。

## 3. 已完成阶段

| 阶段 | 状态 | 产物 |
|---|---|---|
| Phase 0-1 | 完成 | 文献 split 审计、方法登记 |
| Phase 2-5 | 完成 | DLPFC 数据、split 框架、指标冻结 |
| Phase 6 | 完成 | Pilot GO，四判据通过 |
| Phase 7A | 完成 | DLPFC 正式化、多数据集准入、正式统计 |
| Phase 8 | 完成 | Andersson/Thrane 外部 formal benchmark |
| Phase 9 | 完成 | shared_panel_50 三数据集统一目标基准 |
| Phase 10 | 完成 | Visium breast V0.1 |
| Phase 11 | 完成 | final statistics refresh |
| Phase 12 | 完成 | GraphSAGE shared-panel 整合 |
| Phase 13A | 完成 | Andersson-to-Visium dataset-held-out prototype |
| Phase 13B | 完成 | paper result assets |
| Phase 14A | 完成 | manuscript skeleton 与路线决策 |
| Phase 14B | 完成 | Python 初版论文图 |
| Phase 15A-D | 完成 | Results/Methods draft、软件/参数表、引用候选、citation placement map |

## 4. 关键结果

### Dataset-specific targets

| Dataset | Model | Random | Strict split | Strict | RLI |
|---|---|---:|---|---:|---:|
| DLPFC | PCA+Ridge | 0.292 | patient-held-out | 0.230 | 0.213 |
| Andersson | PCA+Ridge | 0.604 | patient-held-out | 0.204 | 0.662 |
| Thrane | PCA+Ridge | 0.653 | patient-held-out | 0.327 | 0.499 |
| Visium breast | Spatial kNN | 0.649 | matched_hop5 | 0.132 | 0.796 |

### shared_panel_50

| Dataset | Model | Random | Patient-held-out | RLI_patient |
|---|---|---:|---:|---:|
| DLPFC | PCA+Ridge | 0.108 | 0.081 | 0.251 |
| Andersson | PCA+Ridge | 0.261 | 0.096 | 0.632 |
| Thrane | PCA+Ridge | 0.317 | 0.113 | 0.644 |

### GraphSAGE shared-panel

| Dataset | Strict split | Random | Strict | RLI |
|---|---|---:|---:|---:|
| DLPFC | matched_hop0 | 0.151 | 0.094 | 0.378 |
| Andersson | matched_hop0 | 0.251 | 0.233 | 0.072 |
| Andersson | patient-held-out | 0.251 | 0.077 | 0.692 |

### Dataset-held-out stress test

Andersson HER2+ breast ST v1.0 -> 10x Visium breast:

- Target panel: shared_panel_50, 49/50 usable targets.
- Missing target: `SEPT4` absent from Visium.
- Model: PCA+Ridge only.
- Result: mean Pearson 0.199 +/- 0.001 across five seeds.
- Interpretation: feasible but weak cross-platform signal; supplementary stress test, not patient-level external validation.

## 5. 机制解释

1. **Spatial-neighborhood leakage**  
   DLPFC 和 Visium breast 中，Spatial kNN / GraphSAGE 对 spatial-buffer split 明显敏感。Visium breast 最强，Spatial kNN 从 random 0.649 降到 matched_hop5 0.132。

2. **Patient/batch shortcut**  
   Andersson 和 Thrane 中，patient-held-out loss 很大。shared-panel 和 GraphSAGE 结果都支持该渠道。

3. **平台密度边界**  
   Visium 高密度平台能显示强 spatial kNN 信号；ST v1.0 低密度数据中 spatial kNN 接近 0，高 hop split 甚至不可解析。

4. **Slide-held-out 不等于 patient-held-out**  
   Visium breast 只有一个 patient，两张 section 的 slide-held-out 只能说明相邻切片共享可迁移组织结构，不能作为 patient-level external validation。

5. **Moran 解释已重写为分渠道**  
   pooled GO-D 方向仍可保留，但 final mixed-effects 显示 patient-channel 不由 per-gene Moran 解释。论文中应明确区分 patient/batch shortcut 与 within-section spatial leakage。

## 6. 主要文件

### 状态与总览

- `CURRENT_STATUS.md`
- `PROJECT_STATUS.md`
- `NEXT_ACTIONS.md`
- `ANALYSIS_LOCK.md`

### 论文草稿

- `docs/reports/MANUSCRIPT_SKELETON.md`
- `docs/reports/MANUSCRIPT_RESULTS_METHODS_DRAFT.md`

`MANUSCRIPT_RESULTS_METHODS_DRAFT.md` 已包含:

- one-sentence argument
- terminology ledger
- Results prose
- Methods prose
- reproducibility parameter table
- software environment table
- statistical interpretation note
- citation-ready Introduction scaffold
- citation-ready Discussion scaffold
- reference audit candidates
- citation placement map
- claim-evidence map

### 论文图与图源

- `scripts/make_paper_figures.py`
- `results/paper_assets/PAPER_RESULT_ASSETS.md`
- `results/paper_assets/table_dataset_specific_RLI.csv`
- `results/paper_assets/table_shared_panel50_RLI.csv`
- `results/paper_assets/table_graphsage_shared_panel50_RLI.csv`
- `results/paper_assets/table_dataset_heldout_anderson_to_visium.csv`
- `results/paper_assets/figure_distance_curve_data.csv`
- `results/paper_assets/figures/fig1_leakage_overview.svg`
- `results/paper_assets/figures/fig1_leakage_overview.png`
- `results/paper_assets/figures/fig2_spatial_distance_curves.svg`
- `results/paper_assets/figures/fig2_spatial_distance_curves.png`
- `results/paper_assets/figures/fig3_model_and_transfer.svg`
- `results/paper_assets/figures/fig3_model_and_transfer.png`
- `results/paper_assets/figures/FIGURE_PACKAGE_NOTES.md`

### 关键报告

- `docs/reports/FINAL_STATS_REFRESH.md`
- `docs/reports/GRAPHSAGE_SHARED_PANEL_REPORT.md`
- `docs/reports/DATASET_HELDOUT_PROTOTYPE.md`
- `docs/reports/DLPFC_FORMALIZATION_REPORT.md`
- `docs/reports/MULTIDATASET_BENCHMARK_V0.1.md`
- `docs/reports/STATISTICAL_ANALYSIS_REPORT.md`
- `docs/literature/SPLIT_AUDIT.md`

## 7. 已冻结方法决策

- LI = `Perf_random - Perf_strict`
- RLI = `LI / Perf_random`
- Retention = `Perf_strict / Perf_random`
- shared_panel_50 在性能计算前冻结。
- 不用 test 结果调参。
- 不 cherry-pick seed 或数据集。
- 空 test split 必须报告为 non-resolvable。
- spot-level confidence intervals 不用于正式统计。
- Spatial kNN 的 RLI 在 random denominator 接近 0 时不解释。

## 8. 已验证状态

最近一次检查:

- `pytest`: 7/7 PASS
- Python paper figures 已生成。
- PNG 视觉 QA 通过。
- SVG 保留 editable text。
- manuscript draft package 无 TODO/TBD/明显夸大词。

## 9. 当前阻塞点

现在不是技术阻塞，而是投稿信息缺失。下一步需要用户提供:

1. 目标期刊。
2. word limit。
3. abstract format。
4. reference style。
5. author list。
6. affiliations。
7. funding。
8. competing interests。
9. data availability。
10. code availability。

收到这些信息后，下一步可以把 `MANUSCRIPT_RESULTS_METHODS_DRAFT.md` 转成正式 manuscript，并插入已审计引用。

## 10. 后续推荐路线

1. 用户确认目标期刊和作者/声明信息。
2. 将 citation candidates 转成目标期刊格式。
3. 把 Introduction/Discussion scaffold 扩成完整正文。
4. 合并 Abstract、Results、Methods、Discussion、Declarations。
5. 生成 DOCX 或 LaTeX manuscript。
6. 暂不加入额外 SOTA，除非目标期刊策略或用户决定要求补充。

## 11. 最短交接句

项目已经完成到 manuscript draft package：数据、统计、图、Results/Methods 草稿、Introduction/Discussion scaffold、引用候选和方法参数表都已就绪。下一步必须等用户给目标期刊和作者/声明信息，才能进入正式投稿稿件生成。
