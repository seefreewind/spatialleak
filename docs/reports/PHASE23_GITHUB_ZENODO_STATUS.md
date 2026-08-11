# Phase 23 GitHub and Zenodo Status

Date: 2026-08-11

## GitHub

Status: complete.

- Repository: https://github.com/seefreewind/spatialleak
- Visibility: public
- Default branch: `main`
- Release: https://github.com/seefreewind/spatialleak/releases/tag/v1.0.0
- Tag: `v1.0.0`

The public repository contains the submission-ready source code, scripts, configs, tests, frozen result tables, source-data files, manuscript materials and Nature Communications draft files. Raw public datasets, processed `.h5ad` objects, logs, rendered QA images and TIFF exports are excluded.

## Zenodo

Status: blocked by user authentication.

The Zenodo GitHub integration page redirects to:

`https://zenodo.org/login/?next=%2Faccount%2Fsettings%2Fgithub%2F`

Zenodo requires the account holder to log in and authorize/connect GitHub before `seefreewind/spatialleak` can be enabled for automatic release archiving. After the repository is enabled in Zenodo, the existing GitHub release `v1.0.0` should be selected or reprocessed to mint the Zenodo DOI.

Official workflow checked:

- https://help.zenodo.org/docs/github/enable-repository/
- https://help.zenodo.org/docs/github/archive-software/github-upload/

## Manuscript Metadata Lock

- Funding: `No specific funding was received for this work.`
- Acknowledgements: omitted, per user instruction.
- Competing interests: no competing interests declared.
- Correspondence: Da Lin, 212574@wzhealth.com; ORCID 0009-0009-4410-0218.

## User Action Required

1. Log in to Zenodo.
2. Open the Zenodo GitHub integration/settings page.
3. Click `Sync now` if `seefreewind/spatialleak` is not listed.
4. Toggle `seefreewind/spatialleak` to enabled.
5. Select or reprocess GitHub release `v1.0.0`.
6. Copy the issued Zenodo DOI back into the manuscript Data Availability / Code Availability text.
