# Clarity Playbook: Easy to Follow, Nothing Ambiguous

The main goal of this skill is that readers understand the work without rereading and without guessing. This file is the working method. It complements `docs/prompt.md` and uses the brief from `docs/project-intake.md`.

## Contents
1. Reader model and the first-pass test
2. Paragraph protocol
3. Ambiguity patterns and repairs
4. Flow and the reverse outline
5. Tense conventions
6. Technical clarity
7. Equations, tables, and metric narration
8. Explaining dense content for mixed readers
9. Reviewer-proofing
10. Before and after

## 1. Reader model and the first-pass test

Write for three readers at once: a **reviewer** hunting for the contribution and validity, a **domain researcher** who wants to reproduce it, and an **adjacent technical reader** who needs definitions.

First-pass test: after reading only the abstract, introduction, and conclusion, each reader should be able to state the problem, the gap, the contribution, the main idea of the method, the main result with its scope, and one limitation. If one of those is missing or unclear, fix that before polishing sentences.

## 2. Paragraph protocol

1. Decide the paragraph's single job: claim, mechanism, prior work, procedure, result, interpretation, or limitation.
2. State that job early, usually in the first sentence. A brief context-setting opener is acceptable when it helps the argument rather than delaying the point.
3. Follow with evidence, steps, or explanation in the order the reader needs them.
4. Add the "so what" only when it contains information (a consequence, a scope, a link the next paragraph needs).
5. If a paragraph has two unrelated jobs, split it. If two paragraphs do the same job, merge them.

## 3. Ambiguity patterns and repairs

| Pattern | Problem | Repair |
|---|---|---|
| "This", "it", "these", "they" with two possible referents | Reader guesses | Repeat the noun: "This penalty term..." |
| Comparison without referent: "better", "faster", "more accurate" | Than what, on which metric, by how much? | "[Metric] is [X] points higher than [named baseline] on [dataset]" |
| Percent versus percentage points | Absolute and relative gains get confused | State which: "3.8 percentage points" or "a 5% relative gain" |
| "Respectively" over long lists | Reader must count | Give explicit pairs, or a small table |
| "The former", "the latter" | Reader scrolls back | Use the names |
| Scope of negation: "does not always improve" | Never, or sometimes? | State when it improves and when it does not |
| Misplaced "only", "also", "even" | Shifts the meaning | Place it directly before what it modifies |
| "And/or" | Inclusive or exclusive? | Choose, or write "A, B, or both" |
| Dangling modifier: "Using X, the accuracy improved" | Who used X? | "Using X, we improved accuracy..." or "With X, accuracy improved" |
| Noun piles of four or more abstract nouns | Parse failure | Use prepositions: "the ability to detect risk in unseen domains" |
| Passive that hides a needed actor: "Outliers were removed" | By which rule? | "We removed samples more than [k] SD from the mean [criterion]" |
| "Significant" | Statistical or large? | Use "statistically significant" with the test, or "large" with the number |
| "Robust", "efficient", "effective", "accurate" without a measure | Unverifiable | Name the measure and value, or drop the word |
| Undefined acronym or symbol; one symbol with two meanings | Confusion | Define at first use; one symbol, one meaning; notation table if over about 10 symbols |
| Term drift: framework, approach, model, method for one thing | Reader suspects different things | Use the locked name |
| "Existing methods" with no names | Unverifiable | Name the baselines and cite them |
| "As shown above", "the figure", "the table" | Which one? | "Figure 3", "Table 2" |
| Long sentence with nested conditions | Logic hidden | Split along the logic: condition, then consequence |
| Mixed tenses inside one paragraph | Unclear what was done versus what is true | Apply section 5 |

## 4. Flow and the reverse outline

- Choose a connector by the relation: cause (because), consequence (therefore), contrast (however, whereas), condition (if, under this assumption), example (for example), sequence (first, then), evidence (the ablation shows). If no relation exists, no connector is needed.
- Start sentences with what the reader already knows, then add the new fact when this supports the argument. A new topic can start a paragraph; it should not start every sentence.
- **Reverse outline:** write one line per paragraph stating its job. Read the lines in order. They should form an argument: problem, gap, idea, method, evidence, interpretation, limitation. Gaps, repeats, and out-of-order jobs show up immediately.

## 5. Tense conventions (venue style overrides)

- **Past:** what was done and observed: methods, procedures, results ("We trained...", "Accuracy was 0.91...").
- **Present:** established facts, definitions, how the paper is organized, and describing figures and tables ("Figure 3 shows...", "The estimator computes...").
- **Future or modal:** future work only.
- Stay consistent inside a paragraph. Switch tense only when the type of statement changes.

## 6. Technical clarity

- Define before use. Introduce each equation in words, display it, then say what its terms do. Number only equations you refer to.
- Algorithms: state inputs, outputs, and the steps in order; keep names consistent with the text.
- Methods: enough detail to replicate (data, splits, preprocessing, settings, hardware, versions).
- Results: report by metric; compare against named baselines; state variance or the number of runs where available; separate what was observed from why it may have happened.
- Figures and tables: self-contained captions; the text tells the reader what to notice. Do not restate every cell.

## 7. Equations, tables, and metric narration

### Equations

- Introduce the purpose of an equation before displaying it when the reader needs context. Define symbols before or after the equation according to the clearest exposition; there is no required order for every paper.
- State what a new term changes in the method or objective. Prefer a short explanation of the term's consequence over repeating a generic `where X denotes...` sentence for every symbol.
- Preserve the original mathematics. Never alter a formula, symbol, assumption, or equation reference merely to improve prose. If notation seems wrong, flag it for author verification.

### Tables and results

- Lead with the main finding when that makes the paragraph easier to understand; use a table reference naturally within the sentence or at its end. Avoid redundant pairs such as `Table 2 presents... As shown in Table 2...` when one precise reference is enough.
- Name the metric, dataset or setting, comparison method, and difference where available. Distinguish absolute values, percentage points, relative percentages, and statistical significance.
- Do not imply that a method wins on all conditions when a table shows mixed results. Note meaningful exceptions, uncertainty, variance, or negative results.
- Explain only the table entries needed for the argument. Do not rewrite every row as prose or claim a cause that the experiment did not test.
- If `scripts/metric_consistency.py` is available, use a project-specific manifest to check selected result claims against source CSV rows and labeled LaTeX tables/paragraph anchors. A passing check covers those explicit mappings only; it does not verify every reported number.

## 8. Explaining dense content for mixed readers

Use three layers when a mechanism matters: a one-sentence intuition, the precise statement, and the consequence for the result. Skip a layer the audience does not need.

> A split that mixes supported and unsupported claims should look worse to the learner. The objective therefore subtracts an evidence-disagreement penalty from the split gain, so such splits are chosen less often.

## 9. Reviewer-proofing

For each question, answer it in the text or flag the gap in the brief:

- Why this baseline, and was it tuned as carefully as the proposed method?
- Same data splits, same tuning budget, same metrics?
- Variance across seeds or folds; is the difference statistically meaningful?
- Does an ablation support the claimed mechanism?
- Any leakage between training and test data?
- What is the scope of generalization, and what is untested?
- What are the limitations and threats to validity?
- Can others reproduce it (code, data, settings, licenses, ethics)?

## 10. Before and after

Placeholders in brackets must be filled from the project; do not invent them.

**Before** (vague and generic):
> Recent advances in AI have significantly transformed many fields. Our proposed approach leverages a comprehensive framework to enhance performance, demonstrating its effectiveness. Furthermore, it is robust.

**After** (specific, scoped, and checkable):
> [Task] still fails on [specific problem], because [known cause, citation]. We address this with [method name], which [one-sentence mechanism]. On [N] datasets, it raises [metric] by [X] points over [named strongest baseline], and the gain holds across [number of runs]; it does not help on [dataset or condition].

What changed: the first sentence names a problem, the method has one name and one mechanism, the claim has a metric, a baseline, and a scope, and the limitation is stated rather than hidden.
