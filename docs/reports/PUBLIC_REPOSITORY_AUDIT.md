# Public Repository Audit

## Git

`git status` result: `UNAVAILABLE: Command '['git', 'status', '--short']' returned non-zero exit status 128.`

The active workspace is not currently a git repository. No public push was attempted.

## File Risk

- `data/` is approximately 4.0G and should not be committed to the public code repository.
- `results/` is approximately 97M; include paper asset tables and selected small figures only.
- No `.env`, `.pem`, `.key`, `*token*`, or `*secret*` files were detected in the shell audit.
- Avoid committing `__pycache__`, `.pytest_cache`, and any future notebook checkpoints.

## Recommended Public Structure

```text
SpatialLeak/
  README.md
  LICENSE
  CITATION.cff
  environment.yml
  requirements.txt
  configs/
  src/
  scripts/
  tests/
  metadata/
  results/paper_assets/
  figures/
  docs/
```
