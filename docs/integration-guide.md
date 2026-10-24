# Using This Skill in Any Agent Tool

The package is plain Markdown plus optional stdlib-only Python scripts, so any agent that can read files can use it. Tool conventions change often: confirm folder names and file names against each tool's current documentation before relying on them.

## Core idea

1. Put the whole `academic-student-writer/` folder somewhere the agent can read. Never copy only `SKILL.md`; it refers to other files (it is self-sufficient if nothing else can be loaded, but weaker).
2. Make the research project visible to the agent: the manuscript, code, results, data docs, bibliography, notes, and earlier writing.
3. Tell the agent which file to start from. The ready-made stubs in `integrations/` do that for common tools.
4. If the agent can run code, `python scripts/project_scan.py <project_root>` gives it a fast inventory.

## Install by tool

For native skill support, copy the complete `academic-student-writer/` directory to the indicated path. Keep `SKILL.md`, `docs/`, `scripts/`, `templates/`, and `evals/` together. The path before the arrow is project-local; the second path is for a personal installation where supported.

On Windows, `~` means `%USERPROFILE%`. Copy the complete folder into the target directory; do not copy only `SKILL.md` if you want the supporting guides, templates, and scripts to remain available.

| Tool | Project location | Personal or global location | Invoke or enable |
|---|---|---|---|
| OpenCode | `.opencode/skills/academic-student-writer/` | `~/.config/opencode/skills/academic-student-writer/` | Type `@academic-student-writer`. |
| Codex | `.agents/skills/academic-student-writer/` | `~/.agents/skills/academic-student-writer/` | Type `$academic-student-writer` in Codex CLI or IDE; run `/skills` to browse. |
| Claude Code | `.claude/skills/academic-student-writer/` | `~/.claude/skills/academic-student-writer/` | Type `/academic-student-writer`, or let Claude select it from the description. |
| Cline | `.cline/skills/academic-student-writer/` | `~/.cline/skills/academic-student-writer/` | Enable in the Skills menu, type `/academic-student-writer`, or let Cline select it. |
| Roo Code | `.roo/skills/academic-student-writer/` | `~/.roo/skills/academic-student-writer/` | Type `/academic-student-writer` or let Roo select it. Roo also supports `.agents/skills/` and `~/.agents/skills/` for sharing across agents. |

OpenCode also supports `.agents/skills/` and `.claude/skills/` compatibility locations. Codex detects skill changes automatically; restart it if a new skill does not appear. Other tools may require a reload or a new session.

### Claude Projects

Claude Projects use uploaded project knowledge and project instructions, not Claude Code's local skill folder. Add `SKILL.md` and the task-relevant supporting guides to Project knowledge. Paste `integrations/CLAUDE.md` into Project instructions, then ask Claude to use Academic Student Writer. Mention the uploaded documents by file name in your request. Scripts are not runnable through uploaded project knowledge; use Claude Code when the task needs the bundled Python helpers.

### Cursor

1. Copy the full skill folder to `.agents/skills/academic-student-writer/` in your project.
2. Copy `integrations/academic-writer.mdc` to `.cursor/rules/academic-writer.mdc`.
3. Replace `<SKILL_DIR>` in the rule with `.agents/skills/academic-student-writer` (or another path Cursor can read).
4. In Cursor, ask it to use the Academic Student Writer instructions for research-writing tasks.

Cursor rules are instructions, not a native skill command. For global use, add the rule through Cursor's User Rules settings and use a skill folder at a path readable from your projects.

### GitHub Copilot

1. Copy the full skill folder to `.agents/skills/academic-student-writer/` in your project.
2. Copy `integrations/copilot-instructions.md` to `.github/copilot-instructions.md`.
3. Replace `<SKILL_DIR>` in the instructions with `.agents/skills/academic-student-writer` (or another path the agent can read).
4. Ask Copilot to use Academic Student Writer for the task. Custom-instruction support and settings vary by Copilot client.

### Gemini CLI

1. Keep the full skill folder at a path Gemini CLI can read.
2. Copy `integrations/GEMINI.md` to `GEMINI.md` at the project root. For personal global guidance, use `~/.gemini/GEMINI.md` instead.
3. Replace `<SKILL_DIR>` with the skill folder path.
4. Start a new Gemini CLI session and ask it to use Academic Student Writer. Gemini loads `GEMINI.md` as context; it does not use the OpenCode `@` invocation syntax.

### Plain chat without file access

Paste `SKILL.md`, then provide the task-relevant guides and research materials. Include the manuscript, key results, data documentation, bibliography, venue instructions, and author-written samples as appropriate. Tell the model which mode to use. It cannot read the rest of the repository or run the bundled scripts unless those files and tools are separately provided.

For an optional OpenCode slash command, copy `integrations/opencode/commands/academic-student-writer.md` to `.opencode/commands/academic-student-writer.md`. This command is separate from the skill; the native invocation remains `@academic-student-writer`.

If an integration stub contains `<SKILL_DIR>`, replace it with the actual path to the folder before use. Tool conventions change, so check the linked official documentation when upgrading or changing the target runtime:

- [OpenCode skills](https://opencode.ai/v2/docs/skills)
- [Codex skills](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Cursor rules](https://prod.cursor.com/docs/rules)
- [GitHub Copilot custom instructions](https://docs.github.com/en/copilot/concepts/prompting-and-context/custom-instructions?tool=vscode)
- [Gemini CLI context files](https://geminicli.com/docs/cli/gemini-md/)
- [Cline skills](https://docs.cline.bot/customization/skills)
- [Roo Code skills](https://docs.roocode.com/features/skills)

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
