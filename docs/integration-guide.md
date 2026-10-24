# Using This Skill in Any Agent Tool

The package is plain Markdown plus optional stdlib-only Python scripts, so any agent that can read files can use it. Tool conventions change often: confirm folder names and file names against each tool's current documentation before relying on them.

## Core idea

1. Put the whole `academic-student-writer/` folder somewhere the agent can read. Never copy only `SKILL.md`; it refers to other files (it is self-sufficient if nothing else can be loaded, but weaker).
2. Make the research project visible to the agent: the manuscript, code, results, data docs, bibliography, notes, and earlier writing.
3. Tell the agent which file to start from. The ready-made stubs in `integrations/` do that for common tools.
4. If the agent can run code, `python scripts/project_scan.py <project_root>` gives it a fast inventory.

## Per tool

### OpenCode setup (current docs checked 2026-10-24)

1. Copy the whole `academic-student-writer/` folder to your project at `.opencode/skills/academic-student-writer/`, or globally to `~/.config/opencode/skills/academic-student-writer/`. Keep `SKILL.md`, `scripts/`, `docs/`, `templates/`, and `evals/` together.
2. Invoke the skill by writing `@academic-student-writer` in the prompt. OpenCode advertises skills from the description and loads the skill body on demand; companion documents are read only when the instructions call for them.
3. If you prefer `/academic-student-writer`, copy `integrations/opencode/commands/academic-student-writer.md` to `.opencode/commands/academic-student-writer.md`. Slash commands are separate from skills. The bundle does not rely on a `metadata.opencode/slash` frontmatter field.
4. If the skill is not discovered, check the path-derived ID, file name `SKILL.md`, description, current agent's skill permission, duplicate skill IDs, and current OpenCode documentation.

| Tool | Where to put the skill | Entry point |
|---|---|---|
| Claude (claude.ai) | Upload as a skill if your plan allows, or add the folder files to a Project | Ask: "Use the academic-student-writer skill" |
| Claude Code | `.claude/skills/academic-student-writer/` (project) or `~/.claude/skills/` (global) | Skill is discovered by its description; or use `integrations/CLAUDE.md` |
| OpenCode | `.opencode/skills/academic-student-writer/` or `~/.config/opencode/skills/`; compatibility directories `.agents/skills/` and `.claude/skills/` are also supported by current OpenCode docs | `@academic-student-writer` (direct skill invocation). A slash command is optional and requires a separate command file. |
| Codex CLI and other tools that read `AGENTS.md` | Any folder, for example `.agents/skills/academic-student-writer/` | Add `integrations/AGENTS.md` to the repo root |
| Cursor | Any folder in the repo | Copy `integrations/academic-writer.mdc` to `.cursor/rules/` |
| GitHub Copilot (VS Code, CLI) | Any folder in the repo | Add the text of `integrations/copilot-instructions.md` to `.github/copilot-instructions.md` |
| Gemini CLI | Any folder in the repo | Add `integrations/GEMINI.md` to the repo root |
| Cline, Roo, and similar | Any folder in the repo | Copy `integrations/clinerules.md` to `.clinerules` |
| Plain chat (no file access) | n/a | Paste `SKILL.md`, then paste or attach the manuscript, key results, and the brief |

In every stub, replace `<SKILL_DIR>` with the real path to this folder.

## Prompts that work in any tool

Understand first:
> Use the academic-student-writer skill. Read the whole project and produce PROJECT_BRIEF.md and VOICE_PROFILE.md. List conflicts between sources and any questions only I can answer. Do not edit the manuscript yet.

Edit:
> Use the academic-student-writer skill, Mode 1. Edit `paper/main.tex` section 3 for clarity and flow. Preserve all numbers, equations, citation keys, and claim strength. Return revised LaTeX only, and list material questions in Notes.

Draft from evidence:
> Use the academic-student-writer skill, Mode 2. Draft the Results section from `results/` and the brief. Mark missing values with placeholders. State the authorship rung and what I should verify.

Audit:
> Use the academic-student-writer skill, Mode 4. Audit the manuscript against G0-G15, the claim-evidence map, and the clarity playbook. Give findings by severity.

## Notes for tool authors

- Skills load progressively in some tools: metadata first, `SKILL.md` on trigger, other files on demand. The section 9 table in `SKILL.md` says when to load each file.
- Agents need file-reading tools and workspace access for the project-reading step. Without them the skill still works on pasted text, but say what could not be verified.
- Behavior varies by model, context size, and permissions. Test your model with `docs/evaluation-guide.md` before relying on it for a submission.
