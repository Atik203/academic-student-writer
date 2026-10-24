## 3.1.2 (2026-10-24)

- Added directly sourced Turnitin facts to the main skill and detector-awareness guide: current 300-word qualifying-prose requirement, current unified blue English report presentation (2026-08-04), English-model update (2026-10-14), and links to official pages.
- Clearly labeled two historical Turnitin notes: the 2023 under-300-word processing bug and the 2023 false-positive observation for generic opening/closing sentences. They are not described as proof of current model behavior.
- Reworked the Turnitin detector log to distinguish current requirements, current report behavior, dated model updates, historical interface states, historical incidents, and vendor limitations.
- Updated evaluation guidance and regression cases to test current-versus-historical detector facts and require official citations.
- Relaxed rigid paragraph instructions: state the paragraph's purpose early in most cases; scope empirical/comparative claims with applicable fields; do not force project-specific data into conceptual or transitional paragraphs. Clarified that project inventory does not mean every file can or should be fully read, and that large/private data should be inspected safely.
- Replaced an unsupported generalization that generic phrasing is the most common cause of machine-like prose with a qualified writing-quality statement.
- Updated README, prompt metadata and version references for v3.1.2.

# Changelog

## 3.1.1 (2026-10-24)

- Prevented inventory output from copying README prose, raw result rows, or content from file symlinks; absolute root and output paths are omitted.
- Tightened sensitive-filename matching so ordinary files such as `tokenizer.py` remain discoverable, and expanded matching for credential-bearing configuration files.
- Added `scripts/metric_consistency.py` for explicit CSV-to-prose/LaTeX-table checks, with source-path confinement, unique anchor/label checks, and positive/negative fixtures.
- Added advisory diagnostics for repetitive opening families, flat cadence, and paragraphs without explicit relation markers. These are reader-review prompts, not detector predictions or hard pass/fail criteria.
- Restored the supplied guideline's G4 requirements: P1 uses 3–4 relevant cited papers; P2 reviews 5–6 relevant studies in 1–2 sentences each, unless a documented higher-priority override applies. P3/P4 detail unresolved limitations, method/dataset rationale, supported headline outcomes, and contributions.
- Added a three-stage evidence → reviewer-flow → integrity/quality workflow and task-based context routing, with an initial default of up to three guidance files per stage.
- Corrected OpenCode integration: `@academic-student-writer` is the default invocation; an optional slash command is supplied separately. Removed unsupported `metadata.opencode/slash`.
- Updated detector notes to distinguish official release notes, vendor performance claims, independent research, and maintainer inference.
- Added math/table writing guidance and clarification of method-plus-dataset placement.
- Expanded regression tests for privacy, symlink handling, metrics, cadence diagnostics, source-guide requirements, and OpenCode setup.

## 3.1.0 (2026-10-24)
- New `docs/weak-model-playbook.md`: 12 common mistakes with fixes, plain description of what detection tools look at, a "do not fake human traits" rule, step-by-step procedures for Modes 1 and 2, a paragraph builder, phrase replacements, examples, stop rules, and a final yes/no check.
- `SKILL.md` section 6 now includes a plain "how detection tools see text" block, so an agent that loads only this file still gets it; the never-do list now covers filler and invented anecdotes added to seem human.
- `detector-awareness.md` expanded with a conceptual overview of detector signals and a rule against simulating human traits.
- Still no evasion methods: they would compromise quality and research integrity.

## 3.0.0 (2026-10-24)
- `SKILL.md` rewritten to be self-sufficient: goal, non-negotiables, pre-writing checklist, modes, authorship rungs, rules, detector context, audit, priority order.
- Added project intake, voice calibration, clarity playbook, evaluation guide, templates, scripts, eval fixtures, and integration stubs.
- Detector docs split into stable policy (`detector-awareness.md`) and dated vendor facts (`detector-log.md`).

## 2.1.0 (2026-10-23)
- Previous release.
