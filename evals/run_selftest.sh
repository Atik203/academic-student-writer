#!/usr/bin/env bash
# Self-test the integrity, style-diagnostic, project-inventory and metric-audit tools.
# Run from the skill folder: bash evals/run_selftest.sh
set -u
cd "$(dirname "$0")/.."
fail=0
check() { if [ "$2" = "$3" ]; then echo "PASS  $1"; else echo "FAIL  $1 (expected $3, got $2)"; fail=1; fi; }

python3 scripts/integrity_check.py evals/fixtures/latex/original.tex evals/fixtures/latex/edited_good.tex >/dev/null
check "integrity_check accepts a faithful edit" "$?" "0"

python3 scripts/integrity_check.py evals/fixtures/latex/original.tex evals/fixtures/latex/edited_bad.tex >/dev/null
check "integrity_check rejects a damaging edit" "$?" "1"

out=$(python3 scripts/pattern_scan.py evals/fixtures/text/generic_llm_sample.txt)
echo "$out" | grep -q "generic_frames"; check "pattern_scan flags generic frames" "$?" "0"
echo "$out" | grep -q "summary_closers"; check "pattern_scan flags summary closers" "$?" "0"
echo "$out" | grep -q "participial_tails"; check "pattern_scan flags participial tails" "$?" "0"
echo "$out" | grep -q "comparison_without_referent"; check "pattern_scan flags comparison without referent" "$?" "0"

clear=$(python3 scripts/pattern_scan.py evals/fixtures/text/clear_sample.txt)
echo "$clear" | grep -q "generic_frames"; check "pattern_scan leaves clear text without generic frames" "$?" "1"

flat=$(python3 scripts/pattern_scan.py evals/fixtures/latex/edited_flat_cadence.tex)
echo "$flat" | grep -q "repetitive_opening_family"; check "pattern_scan notices mixed but repetitive openers" "$?" "0"
echo "$flat" | grep -q "flat_cadence"; check "pattern_scan notices flat cadence as advisory" "$?" "0"
echo "$flat" | grep -q "DIAGNOSTIC ONLY"; check "pattern findings are explicitly advisory" "$?" "0"
good_cadence=$(python3 scripts/pattern_scan.py evals/fixtures/latex/edited_good.tex)
echo "$good_cadence" | grep -q "flat_cadence"; check "pattern_scan does not flag the good prose fixture for flat cadence" "$?" "1"

good_metric=$(python3 scripts/metric_consistency.py --root . --manifest evals/fixtures/metric_audit/metric-audit.csv >/dev/null 2>&1; echo $?)
check "metric_consistency accepts matching prose and table values" "$good_metric" "0"
bad_prose_metric=$(python3 scripts/metric_consistency.py --root . --manifest evals/fixtures/metric_audit/metric-audit-bad-prose.csv >/dev/null 2>&1; echo $?)
check "metric_consistency rejects mismatch in prose" "$bad_prose_metric" "1"
bad_sentence_metric=$(python3 scripts/metric_consistency.py --root . --manifest evals/fixtures/metric_audit/metric-audit-bad-sentence.csv >/dev/null 2>&1; echo $?)
check "metric_consistency rejects value only present in a different sentence" "$bad_sentence_metric" "1"
bad_table_metric=$(python3 scripts/metric_consistency.py --root . --manifest evals/fixtures/metric_audit/metric-audit-bad-table.csv >/dev/null 2>&1; echo $?)
check "metric_consistency rejects mismatch in LaTeX table" "$bad_table_metric" "1"

scan=$(python3 scripts/project_scan.py evals/fixtures/project_demo)
echo "$scan" | grep -q "unused2020"; check "project_scan finds the unused bib entry" "$?" "0"
echo "$scan" | grep -q "metrics.csv"; check "project_scan lists the results file" "$?" "0"
echo "$scan" | grep -q "Possible secrets"; check "project_scan lists .env as skipped" "$?" "0"
echo "$scan" | grep -q "not-a-real-key"; check "project_scan never prints secret contents" "$?" "1"
echo "$scan" | grep -q "evidence-conditioned gradient boosting"; check "project_scan does not copy README prose into inventory" "$?" "1"

# Regression: inventory must not leak a raw row from a result-like CSV, and a normal
# tokenizer.py source file must not be misclassified as a secret.
tmp=$(mktemp -d)
mkdir -p "$tmp/results" "$tmp/src"
printf 'record_id,email,score\nSYNTHETIC_PRIVATE_SENTINEL,person@example.test,0.91\n' > "$tmp/results/evaluation_scores.csv"
printf 'def tokenize(text): return text.split()\n' > "$tmp/src/tokenizer.py"
private_scan=$(python3 scripts/project_scan.py "$tmp")
echo "$private_scan" | grep -q "SYNTHETIC_PRIVATE_SENTINEL"; check "project_scan never previews raw result rows" "$?" "1"
echo "$private_scan" | grep -q "tokenizer.py"; check "project_scan does not hide tokenizer.py as a secret" "$?" "0"
echo "$private_scan" | grep -Fq "$tmp"; check "project_scan omits the absolute root path" "$?" "1"
echo "$(cat SKILL.md)" | grep -q "opencode/slash"; check "SKILL.md does not rely on unsupported OpenCode slash metadata" "$?" "1"
grep -q '@academic-student-writer' docs/integration-guide.md; check "OpenCode guide documents direct skill invocation" "$?" "0"
test -f integrations/opencode/commands/academic-student-writer.md; check "optional OpenCode slash-command file is included" "$?" "0"
grep -q '3–4 relevant cited papers' docs/writing-guide.md; check "writing guide preserves P1 citation count" "$?" "0"
grep -q '5–6 relevant prior studies' docs/writing-guide.md; check "writing guide preserves P2 study count" "$?" "0"

# Project symlinks must not cause the scanner to read an external manuscript.
# Skip only if this platform or account cannot create symlinks.
outside_file=$(mktemp)
printf '\\section{LINKED_CONTENT_SENTINEL}\n\\begin{abstract}EXTERNAL_SECRET_SENTINEL\\end{abstract}\n' > "$outside_file"
if ln -s "$outside_file" "$tmp/paper.tex" 2>/dev/null; then
  link_scan=$(python3 scripts/project_scan.py "$tmp")
  echo "$link_scan" | grep -q "LINKED_CONTENT_SENTINEL"; check "project_scan does not follow symlinks to external content" "$?" "1"
else
  echo "SKIP  symlink-content test (symlink creation unavailable)"
fi
rm -f "$outside_file"

traversal=$(python3 scripts/metric_consistency.py --root . --manifest ../outside.csv 2>&1)
traversal_code=$?
check "metric_consistency rejects manifest path traversal cleanly" "$traversal_code" "2"
echo "$traversal" | grep -q "Traceback"; check "metric_consistency reports path errors without traceback" "$?" "1"
rm -rf "$tmp"

# Detector claims must be sourced and distinguish current behavior from historical notes.
grep -q 'at least 300 words of qualifying prose' docs/detector-awareness.md; check "detector guide states the current 300-word requirement" "$?" "0"
grep -q 'unified set of blue highlights' docs/detector-awareness.md; check "detector guide states current unified blue presentation" "$?" "0"
grep -q 'Do not describe a separate current purple category' docs/detector-awareness.md; check "detector guide labels old purple distinction as superseded" "$?" "0"
grep -q '2026-08-04' docs/detector-awareness.md; check "detector guide dates the report-presentation change" "$?" "0"
grep -q 'historical vendor-reported issue' docs/detector-awareness.md; check "generic opening/closing concern is labeled historical" "$?" "0"
grep -q '2023-12-15' docs/detector-log.md; check "under-300-word processing bug is dated historical evidence" "$?" "0"
grep -q '2026-10-14' docs/detector-log.md; check "English-model update is dated and sourced" "$?" "0"
grep -q 'AI-bypasser detection' docs/detector-log.md; check "bypasser behavior is recorded with historical/current distinction" "$?" "0"
grep -q 'Official Turnitin facts test' docs/evaluation-guide.md; check "evaluation guide includes Turnitin-fact regression test" "$?" "0"
grep -q '3.1.2' SKILL.md; check "SKILL metadata advertises v3.1.2" "$?" "0"
grep -q 'three-document default' SKILL.md; check "skill retains context-routing guardrails" "$?" "0"
grep -q 'Never imply that every file was read if it was not' SKILL.md; check "project-reading instructions distinguish inventory from deep reads" "$?" "0"

exit "$fail"
