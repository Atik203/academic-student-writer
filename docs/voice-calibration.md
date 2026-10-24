# Voice Calibration: Keep the Text Recognizably the Author's

**Purpose:** Keep drafts and edits consistent with how the author actually writes, so the paper reads as one person's work and the author can stand behind every sentence. This is about ownership and consistency. It is not a way to imitate another person, and it is not a detector tactic.

## Contents
1. Choosing samples
2. Confidence levels
3. Features to extract
4. Applying the profile
5. Output
6. Updating and limits

## 1. Choosing samples

**Use** text the author wrote themselves: earlier reports and thesis chapters, proposal text, project notes, lab-notebook prose, their own drafts in this project (including older versions in version history from before AI assistance).

**Exclude:** papers by other people, the supervisor's text, templates and boilerplate, quotations, and anything written or substantially edited by an AI. Check version history, the AI-use ledger, and file names for hints. If provenance is unclear, ask once: "Which of these files did you write yourself?" If you cannot ask, treat the file as unreliable and say so.

## 2. Confidence levels

| Reliable sample | Confidence | What to do |
|---|---|---|
| Under about 500 words | Low | Use plain, neutral academic English. Record only terminology preferences |
| 500 to 2,000 words | Medium | Apply features that are consistent across the samples |
| Over about 2,000 words across two or more documents | High | Apply the full profile |

State the confidence in the profile. Never build a profile from AI-generated text.

## 3. Features to extract

| Feature | What to record |
|---|---|
| Person and voice | "We", "I", or passive; when each is used |
| Tense habits | Tense for methods, results, background |
| Sentence rhythm | The usual range and what the author does for emphasis. Describe it; do not turn it into a target |
| Paragraph shape | Typical length and how paragraphs open |
| Connectors | The linking words the author really uses; avoid importing ones they never use |
| Hedging | How strongly the author claims and which hedges they use |
| Showing results | How they introduce tables, figures, and numbers |
| Preferred terms | Names for methods, components, metrics; spelling variety (US or UK) |
| Formality and punctuation | Contractions, parentheses, semicolons, em dashes |
| Language issues to fix | Recurring slips in articles, prepositions, tense, agreement, or run-on sentences, stated neutrally |

## 4. Applying the profile

- Mirror the features that help clarity. Keep the author's distinctive, clear phrasing; do not replace it with a uniform house style.
- **Fix** the recurring language issues. Never copy errors or deliberately add them.
- If an author habit causes ambiguity (for example a vague "this"), clarity wins; note it so the author learns the pattern.
- When drafting at rungs C or D, write consistently with the profile, then tell the author which parts they should personally review and rewrite in their own words, especially interpretations and claims.
- A voice profile does not turn AI-written text into the author's work. Authorship still depends on the author's thinking, checking, and revision.

## 5. Output

Fill `templates/voice-profile.md` and save it as `writing-support/VOICE_PROFILE.md`. List the sample files and their word counts so the author can correct the choice of samples.

## 6. Updating and limits

When the author edits your output, learn from the edits: if they repeatedly change X to Y, record that preference. Re-check the profile when new author-written text appears. Do not imitate a specific named person without that person's authorization.
