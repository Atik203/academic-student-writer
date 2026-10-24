# CLAIM_EVIDENCE_MAP.md

List every claim in the abstract, contributions, results, and conclusion.

| # | Claim (as written) | Section | Evidence (file, table, figure, or citation) | Support (direct, partial, none) | Action |
|---|---|---|---|---|---|
| 1 | | | | | keep / soften / scope / remove / needs evidence |

Rules: a claim with support `none` is a Critical finding in an audit and must be removed, softened, or backed. Causal and "novel" or "first" claims need direct evidence or a defined search scope. Check that the same number appears identically in every section that states it.

## Numeric-claim verification

For important claims sourced from CSV metrics, maintain a project-specific `metric-audit.csv` from `templates/metric-audit.csv`. Map the claim to exact CSV filters, the source value column, a unique manuscript paragraph anchor, and/or a labeled LaTeX table. Run `scripts/metric_consistency.py` to compare those explicit values. This script does not discover all claims automatically and does not replace source-provenance review.
