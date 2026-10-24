# Guide Addenda (proposed notes on the supervisor-locked G0-G15)

`docs/writing-guide.md` is the supervisor's guideline and stays unchanged. This file lists gaps and interpretation notes found in review. Nothing here overrides the guide. Items marked **ASK SUPERVISOR** need confirmation before they change structure.

| # | Where | Issue | Handling until confirmed | Status |
|---|---|---|---|---|
| 1 | G10 (5.5), G11 | Limitations have only a thin home (5.5 mentions limitations observed; the conclusion list has none) | Keep limitations inside 5.5 as the guide says; mention the main one briefly in the conclusion if the venue expects it. Never omit limitations the project shows | ASK SUPERVISOR |
| 2 | G13 | No AI-use disclosure line | If the venue or institution requires an AI-use statement, add it to Declarations using `templates/ai-use-ledger.md`. If unknown, ask once | Apply when required |
| 3 | G2 item 6 and its short form | Item 6 says "Expected/Research Outcome"; the short form says "What did you achieve?" | Keep the six-question order. For a finished study, report the actual outcome (key result with metric and scope), not an expectation | Interpretation |
| 4 | Whole guide | No tense convention | Use `docs/clarity-playbook.md` section 5 unless the venue differs | Apply |
| 5 | G4.1 | Paragraph 1 prompts overlap with P2-P4 | Already handled by the interpretation note in G4; use G4.5 to keep paragraph roles separate | Interpretation |
| 6 | G4, article-type table | Related work is merged into Introduction P2 | If the venue requires a separate Related Work section, follow the venue and keep the same critical-gap logic | Follow venue |
| 7 | G9, G10 | No explicit prompt for number of runs, seeds, or variance | Where the project has repeated runs, report them with the results and in the setup | ASK SUPERVISOR |

Record the supervisor's answers here with the date. Once an item is confirmed, move it into the author's project brief (`PROJECT_BRIEF.md`, section "Venue and supervisor constraints") instead of editing the locked guide.


## Release 3.1.1 clarifications (agent notes, not supervisor-source text)

- **Introduction counts (source requirement):** G4.1 calls for 3–4 cited papers supporting the current-state discussion in P1. G4.2 calls for 5–6 relevant prior studies in P2, with 1–2 sentences per study describing its finding and a concrete limitation, followed by the specific gap. These counts are in the supplied guideline, not an added generic template. Follow them unless a documented dated supervisor override or explicit target-venue constraint takes precedence, and record the reason for any deviation.
- **Method + dataset placement:** Treat a dataset-first G6 section and a dataset subsection within Experiments as alternatives based on the paper's contribution type, as explained in G5/G6. If the dataset is itself a primary contribution, give it an early dedicated section. If it is mainly an evaluation resource for a method contribution, keep it in Experiments (for example, §4.2 where that fits the venue). If both are substantial contributions, use the corpus + method structure. Avoid repeating the full dataset account.
- **Source authority:** Do not apply a single source-type ranking without verifying run/version provenance. Use the source most authoritative for the claim type and record disagreements instead of silently selecting a value.
