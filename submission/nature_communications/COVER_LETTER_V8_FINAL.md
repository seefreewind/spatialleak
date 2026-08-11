Dear Editors,

We submit the manuscript entitled "Evaluation design reshapes apparent generalization in spatial omics prediction" for consideration as an Article in Nature Communications. Different evaluation designs in spatial omics do not support equivalent generalization claims, yet predictive model performance is often interpreted without separating local interpolation, section transfer, patient transfer and dataset transfer.

SpatialLeak addresses this problem by defining a leakage-resistant evaluation hierarchy for spatial omics prediction. Across public spatial transcriptomics datasets, the framework separates two sources of apparent generalization: local spatial-neighborhood dependence and subject-associated structure.

The evidence comes from frozen analyses across public datasets. Dense Visium breast data showed strong spatial-neighborhood inflation, GraphSAGE showed subject-associated losses in Andersson and Thrane, and GSE278936 prostate Visium showed that hop0 spatial partitioning was insufficient while non-zero buffers exposed a PCA+Ridge performance drop.

The resulting six-tier hierarchy provides practical guidance for matching split design to the level of generalization being claimed. We believe the manuscript will be relevant to researchers in spatial transcriptomics, computational biology, machine-learning evaluation and reproducible biomedical data science.

All authors have approved this submission. The authors declare no competing interests.

Code and source data are available at https://github.com/seefreewind/spatialleak (v1.0.0) and archived at https://doi.org/10.5281/zenodo.21881438.

Sincerely,

Da Lin
212574@wzhealth.com
