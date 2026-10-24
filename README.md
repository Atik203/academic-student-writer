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

For project-only installation, use `.opencode/skills/academic-student-writer/` inside the project. See the [OpenCode integration notes](docs/integration-guide.md#install-by-tool) for details.

### Other agent tools

Copy the complete skill folder, including `SKILL.md`, `docs/`, `scripts/`, `templates/`, and `evals/`. The paths below are relative to your home directory for personal installs and to your repository root for project installs. On Windows, `~` means `%USERPROFILE%`.

| Tool | Project install | Personal or global install | How to invoke it |
|---|---|---|---|
| [Codex](https://learn.chatgpt.com/docs/build-skills) | `.agents/skills/academic-student-writer/` | `~/.agents/skills/academic-student-writer/` | In Codex CLI or IDE, type `$academic-student-writer`; use `/skills` to browse available skills. |
| [Claude Code](https://code.claude.com/docs/en/skills) | `.claude/skills/academic-student-writer/` | `~/.claude/skills/academic-student-writer/` | Type `/academic-student-writer`, or let Claude select it based on the request. |
| [OpenCode](https://opencode.ai/v2/docs/skills) | `.opencode/skills/academic-student-writer/` | `~/.config/opencode/skills/academic-student-writer/` | Type `@academic-student-writer`. |
| [Cline](https://docs.cline.bot/customization/skills) | `.cline/skills/academic-student-writer/` | `~/.cline/skills/academic-student-writer/` | Choose it from the Skills menu, type `/academic-student-writer`, or let Cline match the request. |
| [Roo Code](https://docs.roocode.com/features/skills) | `.roo/skills/academic-student-writer/` | `~/.roo/skills/academic-student-writer/` | Type `/academic-student-writer` or let Roo match the request. `.agents/skills/` is also supported for cross-agent sharing. |
| [Cursor](https://prod.cursor.com/docs/rules) | Copy the skill folder to `.agents/skills/academic-student-writer/`; copy `integrations/academic-writer.mdc` to `.cursor/rules/academic-writer.mdc`. | Add the rule under Cursor's User Rules and put the skill folder in a readable location. | Ask Cursor to use the Academic Student Writer instructions. Replace `<SKILL_DIR>` in the rule with the skill folder path. |
| [GitHub Copilot](https://docs.github.com/en/copilot/concepts/prompting-and-context/custom-instructions?tool=vscode) | Copy the skill folder to `.agents/skills/academic-student-writer/`; add `integrations/copilot-instructions.md` as `.github/copilot-instructions.md`. | Add the instruction text to your Copilot custom-instructions settings and keep the skill folder at a readable path. | Ask Copilot to use Academic Student Writer. Replace `<SKILL_DIR>` in the instruction text with the skill folder path. |
| [Gemini CLI](https://geminicli.com/docs/cli/gemini-md/) | Copy `integrations/GEMINI.md` to the project root as `GEMINI.md`; keep the skill folder in a readable path. | Add the instructions to `~/.gemini/GEMINI.md` and keep the skill folder in a readable path. | Ask Gemini CLI to use Academic Student Writer. Replace `<SKILL_DIR>` in `GEMINI.md` with the skill folder path. |
| Claude Projects | Add `SKILL.md` and the task-relevant supporting files to Project knowledge; paste `integrations/CLAUDE.md` into Project instructions. | — | Ask Claude to use Academic Student Writer. Claude Projects use uploaded context and project instructions rather than the Claude Code local skill directory. |

For Cursor, Copilot, and Gemini CLI, replace `<SKILL_DIR>` in the integration file with the folder path where you copied the skill. Claude Projects use uploaded files and project instructions instead of a local skill path. Tool support and settings vary by client; see [`docs/integration-guide.md`](docs/integration-guide.md) and the matching file under [`integrations/`](integrations/) for details. If a tool has no file access, use the [plain-chat instructions](docs/integration-guide.md#prompts-that-work-in-any-tool).

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
