# Academic Student Writer

**A research-writing skill for CSE and other technical fields.** It helps an AI agent understand a research project before drafting or editing, keep claims tied to evidence, preserve the author's voice, and make technical writing clearer.

The skill supports papers, theses, reports, abstracts, LaTeX manuscripts, and related research writing. It is designed to work across file-capable agent tools; instructions for each supported tool are in [`docs/integration-guide.md`](docs/integration-guide.md).

## What it does

- Reads project materials such as the manuscript, code, results, data documentation, bibliography, and earlier author-written text before substantive drafting or review.
- Builds a source-linked project brief and a voice profile before writing.
- Supports editing, evidence-grounded drafting, clarity repair, and structured audits.
- Preserves numbers, equations, citation keys, claim strength, and terminology; marks missing facts instead of inventing them.
- Treats AI-writing detector output cautiously and never provides detector-bypass instructions or score guarantees.

## Install

Keep the complete repository together so the skill can access its supporting guides, templates, scripts, and examples.

### OpenCode

Copy the repository to OpenCode's global skills directory:

```text
~/.config/opencode/skills/academic-student-writer/
```

On Windows, the corresponding location is:

```text
%USERPROFILE%\.config\opencode\skills\academic-student-writer\
```

Then invoke it in a prompt with:

```text
@academic-student-writer
```

For project-only installation, use `.opencode/skills/academic-student-writer/` inside the project. See the [OpenCode integration notes](docs/integration-guide.md#opencode-setup-current-docs-checked-2026-10-24) for details.

### Other agent tools

The repository includes setup notes for Claude, Claude Code, Codex and other `AGENTS.md`-based tools, Cursor, GitHub Copilot, Gemini CLI, Cline, Roo, and plain chat. Follow [`docs/integration-guide.md`](docs/integration-guide.md) and use the matching file under [`integrations/`](integrations/).

## First use

Give the agent access to the research project and ask it to understand the evidence before editing. For example:

> Use the academic-student-writer skill. Read the project and produce `PROJECT_BRIEF.md` and `VOICE_PROFILE.md`. List conflicts between sources and questions only I can answer. Do not edit the manuscript yet.

For substantive work, the skill asks the agent to work from evidence, mark unknowns, and follow the venue or supervisor's structure. Choose the requested mode:

| Mode | Use |
|---|---|
| 0 — Understand | Build the project brief and voice profile; identify conflicts and open questions. |
| 1 — Edit and polish | Improve supplied writing while preserving its meaning and claim strength. |
| 2 — Draft from evidence | Draft new text using project evidence and verified sources; mark gaps. |
| 3 — Repair clarity | Rebuild confusing text from its claims, evidence, and sentence relationships. |
| 4 — Audit | Report issues by severity without rewriting the whole manuscript. |

See [`SKILL.md`](SKILL.md) for the complete rules and [`docs/integration-guide.md`](docs/integration-guide.md) for prompt examples.

## Repository contents

- `SKILL.md` — main instructions and task routing.
- `docs/` — project intake, voice calibration, clarity, research structure, evaluation, and detector guidance.
- `templates/` — project brief, voice profile, claim-evidence map, metric audit, and AI-use ledger templates.
- `scripts/` — optional project inventory and writing-integrity utilities.
- `evals/` — example cases and script self-tests.
- `integrations/` — short setup files for agent tools.

The optional Python scripts use the Python standard library and support Python 3.8 or newer. They provide defined checks, not proof that every research claim is correct. Read [`docs/evaluation-guide.md`](docs/evaluation-guide.md) before interpreting results.

## Research integrity and privacy

The skill does not invent findings, citations, methods, metrics, or explanations. It does not help hide AI involvement or evade an institution's disclosure rules. Detector estimates are not proof of authorship, and the skill does not promise a detector score.

Do not submit confidential manuscripts, participant data, credentials, or other sensitive material in public issues or pull requests. Follow the repository's [`SECURITY.md`](SECURITY.md) for vulnerability reports and your institution's rules for research data and AI use.

## Contributing

Bug reports, documentation improvements, and carefully scoped contributions are welcome. Read [`CONTRIBUTING.md`](CONTRIBUTING.md) before opening an issue or pull request. Contributions must preserve evidence fidelity and must not add detector-evasion instructions.

## License

This project is licensed under the [MIT License](LICENSE).
