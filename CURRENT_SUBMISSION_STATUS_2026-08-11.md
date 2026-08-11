# SpatialLeak Current Submission Status

Date: 2026-08-11

## Status

SpatialLeak is in final Nature Communications submission hardening. No new experiments should be added before initial submission.

## Completed in This Lock

- Zenodo DOI and GitHub v1.0.0 availability are present in Data Availability and Code Availability.
- Figure 2 now defines error bars as ±1 s.d. and distinguishes 10 frozen seeds from held-out patient/donor groups.
- Figure 4 now defines error bars as ±1 s.d. across frozen seeds: 10 seeds for DLPFC and Visium breast, 5 seeds for GSE278936.
- Figure 2 source data now includes `random_error_bar`, `strict_error_bar`, `random_n` and `strict_n`.
- Figure 4 source data now includes `sd`, `error_bar` and `n_seeds`.
- Source Data is reduced to the final submission map: Figure 1, Figure 2, Figure 3, Figure 4 and Supplementary Fig. 1.
- Abstract no longer carries the training-only preprocessing phrase.
- Code Availability no longer says the code is prepared for release; it states the public GitHub and Zenodo archive directly.
- Introduction wording around references [2,15,4] was narrowed so it does not overclaim that every cited study used the same random split protocol.
- Supplementary Information now includes dataset/sample structure, split counts, non-resolvable cases, shared_panel_50 robustness, sample-size-matched controls, full per-seed/per-fold outputs, mixed-effects outputs, Moran analysis, GraphSAGE parameters and the Andersson-to-Visium stress test.
- Cover letter and reporting/checklist drafts were updated for the final availability and source-data state.

## Primary Files

- Manuscript DOCX: `submission/nature_communications/SpatialLeak_NatCommun_V8.docx`
- Clean manuscript Markdown: `submission/nature_communications/SpatialLeak_NatCommun_V8_clean.md`
- Supplementary Information: `submission/nature_communications/Supplementary_Information_V3.md`
- Cover letter: `submission/nature_communications/COVER_LETTER_V8_FINAL.md`
- Reporting drafts: `submission/nature_communications/reporting/`
- Source data: `submission/nature_communications/source_data/`

## Verification

- DOCX rendered successfully to 12 page images in `submission/nature_communications/rendered_v8_final_lock/`.
- Visual QA checked title/abstract page, Figure 1, Figure 2, Figure 3, Figure 4 and availability statements.
- Final submission files passed placeholder, stale-phrase, acknowledgement-section and abnormal-Unicode checks.
- Unit tests passed: 7 passed.

## Remaining Human Step

Submit the V8 package to Nature Communications and use:

- GitHub: `https://github.com/seefreewind/spatialleak`
- Zenodo DOI: `https://doi.org/10.5281/zenodo.21881438`

Do not add datasets, models, seeds, target panels or new sensitivity analyses before submission unless an editor or reviewer requests them.
