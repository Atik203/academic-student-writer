# Academic Student Writer v3.1.2

An agent skill for clear, accurate, unambiguous research writing. The agent first reads the whole research project (manuscript, code, results, data docs, bibliography, earlier writing), builds a project brief and a voice profile, then drafts, edits, clarifies, or audits in the author's own voice. It includes detector awareness so that the agent writes from evidence and never games a detector.

## Start here

1. Copy this whole folder where your agent can read it (see `docs/integration-guide.md` for Claude, Claude Code, OpenCode, Codex, Cursor, Copilot, Gemini CLI, Cline, or plain chat).
2. Make the research project visible to the agent.
3. Use the first prompt in `docs/integration-guide.md` ("understand first"), then ask for edits, drafts, or audits.

## Files

| Path | Purpose |
|---|---|
| `SKILL.md` | Entry point. Self-sufficient: goal, non-negotiables, pre-writing checklist, modes, rules, detector context, audit, priorities |
| `docs/project-intake.md` | How agents read the project and build the brief |
| `docs/voice-calibration.md` | How agents learn the author's voice from the author's own writing |
| `docs/clarity-playbook.md` | Ambiguity patterns, flow, tense, reviewer-proofing |
| `docs/weak-model-playbook.md` | Plain-language mistakes list, procedures, paragraph builder, and examples for smaller or less capable agents |
| `docs/prompt.md` | Detailed prose, citation, technical rules and examples |
| `docs/writing-guide.md` | Supervisor-derived G0-G15 structure guide, with project-specific details excluded and interpretation notes documented separately |
| `docs/guide-addenda.md` | Proposed notes on gaps in the locked guide |
| `docs/detector-awareness.md` | Stable detector and authorship policy |
| `docs/detector-log.md` | Dated vendor facts with verification status |
| `docs/evaluation-guide.md` | Rubric and regression tests |
| `docs/integration-guide.md`, `integrations/` | Setup for many agent tools |
| `templates/` | Project brief, voice profile, AI-use ledger, claim-evidence map, metric-audit manifest |
| `scripts/` | `project_scan.py`, `integrity_check.py`, `pattern_scan.py`, `metric_consistency.py` (Python 3.8+, stdlib only) |
| `evals/` | Regression cases, privacy and metric-audit fixtures, and `run_selftest.sh` for the scripts |

## Design choices

- The agent reads the project instead of interviewing the author, and asks only what the files cannot answer.
- Source authority depends on the claim type and the run/version provenance. The skill records conflicts rather than applying a universal file-type ranking.
- Pattern-level checks (generic frames, summary-closers, participial tails, vague quantifiers) come before the word avoid-list, and none of them is a quota or ban.
- Authorship rungs A-D make the policy and detector risk of each workflow explicit.
- The skill does not promise detector scores and does not provide bypass methods. Detector context exists so the agent writes specific, grounded, author-voiced text and records its process honestly.

## Quick checks

```bash
bash evals/run_selftest.sh
python scripts/project_scan.py <project_root> --out writing-support/PROJECT_INVENTORY.md
python scripts/integrity_check.py original.tex edited.tex
python scripts/pattern_scan.py section.tex
python scripts/metric_consistency.py --root <project_root> --manifest writing-support/metric-audit.csv
```

## Limits

The scripts make defined checks; they do not prove every claim is true. Project inventory output lists metadata and paths, not README excerpts or raw result rows. The metric audit checks only explicitly mapped claims in the supplied manifest. No skill can guarantee identical behavior across models. Test your actual model and runtime with `docs/evaluation-guide.md`. No detector result is proof of authorship, and no writing rule can guarantee a score. Follow your institution's AI-use and disclosure policy.
