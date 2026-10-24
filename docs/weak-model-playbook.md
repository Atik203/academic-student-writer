# Direct Instructions for Smaller or Less Capable Agents

Read `SKILL.md` first, then this file. Follow the procedures literally. Do not skip steps because the text "looks fine". If a step cannot be done, say so and use a placeholder. Never fill a gap by guessing.

## Contents
1. The 12 mistakes weaker agents make
2. What detection tools look at (plain version)
3. Do not fake human traits
4. Procedure for Mode 1 (edit)
5. Procedure for Mode 2 (draft)
6. Paragraph builder
7. Phrase replacements
8. Before and after examples
9. Stop rules
10. Final check

## 1. The 12 mistakes weaker agents make

| # | Mistake | Do instead |
|---|---|---|
| 1 | Writing without reading the project files | Read the files first (`docs/project-intake.md`). Write only from them |
| 2 | Inventing numbers, datasets, baselines, or citations to sound specific | Use a placeholder such as `[METRIC VALUE NEEDED]`. A visible gap is correct |
| 3 | Opening with a sweeping statement ("In today's rapidly evolving world...") | Open with the concrete problem or result from the project |
| 4 | Ending every paragraph with a summary sentence ("Overall, this shows...") | End on the last real claim. Add a closing sentence only if it adds information |
| 5 | Starting many sentences with Furthermore, Moreover, Additionally | Use a connector only when it names a real relation (cause, contrast, condition) |
| 6 | Using several names for one thing (framework, approach, method, paradigm) | Use the single name from the terminology lock |
| 7 | Using "this" or "it" when two things could be meant | Repeat the noun |
| 8 | Writing "better", "faster", "significant" with no baseline, metric, number, or test | Give the baseline, metric, value, and test, or remove the claim |
| 9 | Rewriting the whole text when only a few sentences were unclear | Make the smallest edit that fixes the problem. Keep the author's clear wording |
| 10 | Changing numbers, equations, citation keys, labels, or claim strength | Never. Run `scripts/integrity_check.py` after every edit |
| 11 | Making the text sound "more human" by adding errors, odd words, or filler | Never. See section 3 |
| 12 | Promising that text will pass a detector | Never promise a score. Say what you did to improve clarity and grounding |

## 2. What detection tools can and cannot tell you (plain version)

- Detectors estimate whether text resembles examples learned by a specific classifier. They do not directly observe who wrote a passage, whether its claims are true, or whether the author understands the work.
- Results vary by product, version, language, document length, genre, and whether a text combines human and AI contributions. False positives and false negatives are possible.
- Vendors do not publish every internal feature or decision rule. Generic phrases, repetitive structures, and awkward paraphrases are useful **writing-quality review targets**, not reliable predictors of a particular detector score.
- Some products report passages associated with AI-assisted paraphrasing. Check the current official product documentation before making tool-specific claims.

What this means for writing: ground the paragraph in project evidence, preserve the author's terminology and voice, and make each logical connection clear. These practices improve the manuscript; they do not guarantee a detector result. Never add errors or artificial variation to imitate human authorship.

## 3. Do not fake human traits

Human writing differs because the author knows the data, made decisions, hit problems, and cares about some points more than others. Those differences come from real content. You cannot copy them by imitation.

Never:
- add typos, grammar errors, or odd punctuation;
- add random sentence-length changes, filler words, or "casual" asides;
- invent personal stories, failed experiments, or decisions that are not in the project;
- swap words for rare synonyms, or translate the text out and back;
- use Unicode lookalikes or hidden characters;
- run the text through any humanizer or paraphraser.

These can make the text worse and do not provide reliable detector control. They are also dishonest. If the project contains a real failed attempt, a real limitation, or a real design decision, use it. If it does not, leave a placeholder or ask the author.

## 4. Procedure for Mode 1 (edit)

Use the same three stages as `SKILL.md`: (1) preserve evidence and structure, (2) revise reviewer flow, and (3) run integrity and advisory checks. Do not try to solve every goal in one rewrite.

1. Read the whole passage. Write one line stating the job of each paragraph.
2. Read the brief and voice profile. If none exist, follow `SKILL.md` section 3 or say they are missing.
3. Mark only the problems: ambiguous "this/it", terms that drift, claims with no scope, long sentences, wrong tense, a paragraph with two jobs, generic frames, unneeded connectors.
4. Fix each problem with the smallest change. Keep clear author wording.
5. Do not change numbers, equations, citation keys, labels, units, or claim strength.
6. Run `python scripts/integrity_check.py ORIGINAL EDITED`. If it reports CRITICAL, undo that change.
7. Run `python scripts/pattern_scan.py EDITED`. For each hit, ask what specific thing the sentence says. Fix it from project facts, or leave it. Do not chase zero hits.
8. Return the revised text. Add Notes only for ambiguity or author decisions.

## 5. Procedure for Mode 2 (draft)

Use three stages: first assemble the evidence-backed argument, then revise the flow and explanations, then run the mechanical checks. Do not write a polished-sounding claim before locating its evidence.

1. Name the rung (SKILL.md section 4). If it is C or D, give the disclosure reminder once.
2. Open `PROJECT_BRIEF.md`. List the claims this section must make and the evidence for each. A claim with no evidence gets a placeholder.
3. Plan the paragraphs with the reverse outline: one line per paragraph, one job each.
4. Write each paragraph with the paragraph builder (section 6).
5. Use the terminology lock. Use the voice profile if one exists.
6. Put numbers only from result files. Copy them exactly.
7. Do the final check (section 10).
8. List `Items to Confirm`: placeholders and assumptions only.

## 6. Paragraph builder

Fill each slot from the project. If a slot has no evidence, write the placeholder and keep going.

1. **Job:** claim, mechanism, prior work, procedure, result, interpretation, or limitation.
2. **Opening sentence:** the concrete point, using the locked terms. Not a sweeping statement.
3. **Support:** the evidence anchor: dataset, number with metric and baseline, equation or figure reference, citation, or design decision and its reason.
4. **Scope:** where it holds and where it does not.
5. **Close:** the last real claim, or a limit, or a link the next paragraph needs. No summary sentence.

## 7. Phrase replacements

| Avoid | Write instead |
|---|---|
| plays a crucial role in | state what it does: "[X] determines [Y]" with a citation or result |
| in today's rapidly evolving... | the concrete problem: "[Task] still fails on [case] because [cause]" |
| a wide range of | the actual list or count |
| significantly better | "[X] points higher than [baseline] on [metric]" and the test, if run |
| robust | "[metric] changed by less than [X] across [Y] runs" |
| novel | "unlike [named prior work], we [specific difference]" |
| leverages / harnesses | uses |
| demonstrating its effectiveness | "[metric] rose from [A] to [B]" |
| Overall, / In summary, (closing every paragraph) | delete, unless it adds information |
| not only X but also Y | "X and Y", or keep the one that matters |
| Furthermore / Moreover / Additionally | delete, or use the real relation: "because", "however", "for example" |

## 8. Before and after examples

Placeholders in brackets must come from the project.

**Introduction opener.**
Before: "Recent advances in AI have significantly transformed many fields."
After: "[Task] models still produce [specific failure] on [data type], which [consequence for users]."

**Results sentence.**
Before: "Our method achieves better performance than existing approaches."
After: "On [Dataset], [method] reaches [value] [metric], [X] points above [named baseline] ([Table N])."

**Limitation.**
Before: "Further research may explore additional datasets."
After: "We tested only [N] datasets from [domain]; results on [other setting] are untested."

**Ambiguous reference.**
Before: "The encoder changes the representation after normalization. This improves it."
After: "The encoder changes the representation after normalization. [This change / Normalization / The new representation] improves [metric]." Choose the true referent from the project, or ask.

## 9. Stop rules

Stop and ask the author, or use a placeholder, when:
- a number, dataset detail, or citation is not in the project files;
- two sources disagree and you cannot tell which is final;
- a claim needs causal explanation that no ablation supports;
- you do not know the venue's word limit or AI-use rule and it matters;
- the task would require you to hide AI use or to change a detector score.

## 10. Final check

Answer yes or no. Fix every "no" before returning.

1. Is every number, name, and citation from the project or marked for verification?
2. Did the integrity check show no CRITICAL difference?
3. Does each substantive paragraph have one clear main job and an appropriate evidence or reasoning anchor where needed? Do not force a project-specific anchor into a transition or conceptual paragraph.
4. Is each concept named one way throughout?
5. Is every "this/it" and every comparison unambiguous?
6. Does no paragraph end with an empty summary sentence?
7. Are there no typos, odd words, or filler added on purpose?
8. Did I state the authorship rung and avoid promising a score?
