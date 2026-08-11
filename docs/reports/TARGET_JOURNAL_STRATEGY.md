# Target Journal Strategy

Date: 2026-08-10

Sources checked on 2026-08-10:

- Genome Biology publication fee and scope: https://link.springer.com/journal/13059/how-to-publish-with-us and https://genomebiology.biomedcentral.com/
- Nature Communications APC and journal information: https://www.nature.com/ncomms/open-access and https://www.nature.com/ncomms/journal-information
- Bioinformatics OA page: https://academic.oup.com/bioinformatics/pages/open-access
- Briefings in Bioinformatics OA page and home page: https://academic.oup.com/bib/pages/open-access and https://academic.oup.com/bib
- Patterns author / aims pages: https://www.cell.com/patterns/information-for-authors/publishing-options and https://www.cell.com/patterns/aims
- Journal of Biomedical Informatics APC / scope pages: https://www.sciencedirect.com/journal/journal-of-biomedical-informatics and https://amia.org/news-publications/journals/journal-biomedical-informatics

## Comparison

| Journal | Scope fit | Novelty threshold | Dataset/model expectation | Format / OA implication | Main reviewer risk | Required adaptation |
|---|---|---|---|---|---|---|
| Genome Biology | Strong if framed as a spatial omics benchmark with practical evaluation recommendations | High; needs broad genomics relevance and clear reusable resource | Multiple public datasets are good; may ask for more SOTA breadth | Fully OA; official current APC listed as GBP 3,790 / USD 5,690 / EUR 4,690 | "Is this broad enough beyond prediction?" | Emphasize evaluation hierarchy, public resource, and claim-evidence rigor; keep SOTA absence defensible |
| Nature Communications | Possible if the two-channel concept is framed broadly and Figure 1 is strong | Very high; needs cross-field conceptual clarity | Existing breadth may be adequate if story is clean; reviewers may request more model classes | Fully OA; official current APC listed as GBP 5,490 / USD 7,350 / EUR 6,150 | "Is this incremental benchmark work?" | Lead with two-channel framework and leakage-vs-transportable-biology distinction; polish figures heavily |
| Bioinformatics | Strong methods/benchmark fit | Moderate-high; values clear benchmark, reproducibility, tool framing | Current model breadth likely acceptable if method contribution is evaluation design | Fully OA per OUP page; official page notes ISCB member discount, but APC amount was not reliably captured in the accessible page text | "Where is the software/tool?" | Emphasize SpatialLeak as reproducible benchmark framework; include code availability and structured abstract |
| Briefings in Bioinformatics | Good if positioned as benchmark/resource/method paper rather than review | High but less broad-audience pressure than Nat Commun | May accept evaluation framework with strong discussion | Fully OA since 2024; official OA page lists APC categories but accessible text did not expose a stable amount | "Is this a review journal fit?" | Frame as original computational method/resource; consider a broader evaluation checklist angle |
| Patterns | Good for data-science/evaluation framework across biological data | High; wants data-science insight beyond one domain | Current breadth could fit if the conceptual framework is visual and reusable | Open access Cell Press journal; Cell Press page notes APC required; Cell open-access page currently notes a discounted APC program for some articles submitted before 2026-12-31, authors must verify eligibility | "Too domain-specific for broad data science?" | Emphasize general benchmark-dependence lesson and reanalysis value |
| Journal of Biomedical Informatics | Moderate; strongest if framed as biomedical evaluation methodology | Moderate; method validity and general applicability matter | Current spatial omics scope may be narrower than typical biomedical informatics | Hybrid/OA; ScienceDirect lists OA APC USD 3,550 excluding taxes | "Is spatial transcriptomics too omics-specific?" | Broaden introduction to biomedical prediction evaluation and independence assumptions |

## Recommendation

### First-choice strategy

Target Genome Biology or Bioinformatics depending on ambition and appetite for review risk.

- Genome Biology: stronger prestige and genomics fit, but likely demands very polished framing and possibly more external breadth.
- Bioinformatics: best methodological fit and lower risk for a benchmark/evaluation framework manuscript.

### Stretch strategy

Nature Communications is viable only if the manuscript foregrounds the conceptual advance:

> two distinct channels of apparent generalization inflation and an evidence hierarchy for spatial omics prediction.

It should not be submitted as a simple "random split leakage" paper.

### Conservative strategy

Journal of Biomedical Informatics or Patterns could work if the manuscript is reframed around evaluation methodology. Patterns is more attractive than JBI if the figures and conceptual message become broad data-science friendly.

## Pre-Submission Adaptation Checklist

- Genome Biology: make dataset/resource table and reproducibility package very clear.
- Nature Communications: invest in Figure 1 and Discussion D3 on leakage versus transportable biology.
- Bioinformatics: prepare a structured abstract and emphasize code availability.
- Briefings in Bioinformatics: clarify that this is original benchmark research, not a narrative review.
- Patterns: make the evidence hierarchy generalizable beyond spatial transcriptomics without overstating.
- JBI: broaden the independence-assumption framing and reduce genomics-only jargon.

