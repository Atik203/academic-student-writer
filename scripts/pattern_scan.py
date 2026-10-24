#!/usr/bin/env python3
"""Diagnostic scan for generic wording, ambiguity candidates, and flat structure.

Usage:
    python pattern_scan.py FILE [--max 6] [--json]

DIAGNOSTIC ONLY. A hit is a question ("what specific thing does this sentence say?"),
not a defect to delete mechanically. A clean scan proves nothing about quality or about
any detector's verdict. Never edit text to drive the counts to zero, and never use this
output as a score target. Python 3.8+, standard library only.
"""
import argparse
import json
import re
import statistics
import sys

AVOID_WORDS = [
    'tapestry', 'testament', 'realm', 'cornerstone', 'beacon', 'pivotal', 'paramount', 'salient',
    'multifaceted', 'delve', 'deep dive', 'synergy', 'game-changer', 'leverage', 'harness', 'foster',
    'fostering', 'underscore', 'showcase', 'showcasing', 'navigate', 'landscape', 'paradigm',
    'holistic', 'seamless', 'seamlessly', 'comprehensive', 'notably', 'crucial', 'intricate',
    'intricacies', 'interplay', 'meticulous', 'meticulously', 'vibrant', 'enhance', 'bolstered',
    'garner', 'enduring', 'groundbreaking', 'renowned', 'state-of-the-art', 'cutting-edge', 'plethora',
]
FORMAL_OPENERS = ['Furthermore', 'Moreover', 'Additionally', 'Importantly', 'Notably', 'Interestingly',
                  'In addition', 'It is worth noting', 'It is important to note', 'It should be noted']
CLOSERS = ['Overall', 'In summary', 'In conclusion', 'Thus', 'Therefore', 'Hence', 'Collectively',
           'Together', 'Ultimately', 'In essence']
GENERIC_FRAMES = [
    r'plays? an? (?:crucial|vital|pivotal|important|key|significant) role',
    r"in today'?s", r'rapidly (?:evolving|changing)', r'has gained (?:significant|considerable|increasing)',
    r'in the realm of', r'a (?:wide|broad) (?:range|variety|array) of', r'it is (?:important|worth|crucial) to (?:note|mention)',
]
PARTICIPIAL = re.compile(r',\s+(highlighting|demonstrating|ensuring|contributing to|underscoring|showcasing|emphasizing|paving the way)\b', re.I)
NOT_ONLY = re.compile(r'\bnot only\b.*\bbut also\b|\bnot just\b.*\bbut\b', re.I)
VAGUE = re.compile(r'\b(several|various|numerous|a number of|a variety of|multiple|many)\b', re.I)
SIGNIF = re.compile(r'\bsignificant(?:ly)?\b', re.I)
STAT_CUES = re.compile(r'p\s*[<=>]|confidence interval|\bCI\b|t-test|wilcoxon|anova|statistically|effect size', re.I)
COMPARATIVE = re.compile(r'\b(better|faster|slower|higher|lower|superior|more accurate|more efficient|improved|outperform\w*)\b', re.I)
COMPARE_REF = re.compile(r'\bthan\b|\bover\b|compared (?:to|with)|relative to|versus|\bvs\.?\b|baseline|against', re.I)
HEDGE_STACK = re.compile(r'\b(?:may|might|could)\s+(?:potentially|possibly|perhaps)\b|\b(?:potentially|possibly)\s+(?:may|might|could)\b', re.I)
VAGUE_START = re.compile(r'^(This|These|Those|It|They|Such)\s+(is|are|was|were|has|have|had|can|could|may|might|will|would|means|shows|show|allows|leads|makes|helps|enables|improves|reduces|increases|suggests|indicates|ensures)\b')
SYNONYM_SET = ['framework', 'approach', 'paradigm', 'methodology', 'architecture', 'technique', 'strategy', 'scheme']
ABBREV = ['e.g.', 'i.e.', 'et al.', 'Fig.', 'Figs.', 'Eq.', 'Eqs.', 'Sec.', 'vs.', 'cf.', 'approx.', 'No.']


def clean(text, is_tex):
    if is_tex:
        text = re.sub(r'(?<!\\)%.*', '', text)
        text = re.sub(r'\\begin\{(equation\*?|align\*?|gather\*?|multline\*?|eqnarray\*?|tabular\*?|table\*?|figure\*?|lstlisting|verbatim|algorithm\*?|algorithmic)\}.*?\\end\{\1\}', ' ', text, flags=re.S)
        text = re.sub(r'\$\$.+?\$\$|\\\[.+?\\\]|(?<!\\)\$.+?(?<!\\)\$', ' X ', text, flags=re.S)
        text = re.sub(r'\\(?:[a-zA-Z]*cite[a-zA-Z]*|[a-zA-Z]*ref|eqref|label)\*?(?:\[[^\]]*\])*\{[^}]*\}', ' [REF] ', text)
        text = re.sub(r'\\(?:textbf|textit|emph|texttt|section|subsection|subsubsection|paragraph|caption|title)\*?\{([^}]*)\}', r'\1', text)
        text = re.sub(r'\\[a-zA-Z]+\*?(?:\[[^\]]*\])?', ' ', text)
        text = text.replace('{', ' ').replace('}', ' ')
    return text


def sentences(par):
    p = par
    for ab in ABBREV:
        p = p.replace(ab, ab.replace('.', '\u2024'))
    parts = re.split(r'(?<=[.!?])\s+(?=[A-Z\[\(])', p.strip())
    return [s.replace('\u2024', '.').strip() for s in parts if s.strip()]


def snippet(s, n=140):
    s = re.sub(r'\s+', ' ', s)
    return s if len(s) <= n else s[:n - 3] + '...'


def scan(text, is_tex):
    pars = [re.sub(r'\s+', ' ', p).strip() for p in re.split(r'\n\s*\n', clean(text, is_tex))]
    pars = [p for p in pars if len(p.split()) >= 6]
    res = {k: [] for k in [
        'avoid_words', 'formal_openers', 'summary_closers', 'generic_frames', 'participial_tails',
        'not_only_but_also', 'vague_quantifiers', 'significant_without_stats', 'comparison_without_referent',
        'hedge_stacks', 'ambiguous_sentence_starts', 'repeated_openers', 'repetitive_opening_family',
        'flat_cadence', 'zero_explicit_relation_markers', 'long_sentences', 'term_cycling']}
    info = {'paragraphs': len(pars), 'sentences': 0, 'notes': []}
    sent_counts = []
    closers = 0
    for pi, par in enumerate(pars, 1):
        sents = sentences(par)
        sent_counts.append(len(sents))
        info['sentences'] += len(sents)
        for w in AVOID_WORDS:
            for m in re.finditer(r'\b' + re.escape(w) + r'\b', par, re.I):
                res['avoid_words'].append((pi, w, snippet(par[max(0, m.start() - 50):m.end() + 50])))
        if sents and any(sents[-1].startswith(c) for c in CLOSERS):
            closers += 1
            res['summary_closers'].append((pi, 'last sentence', snippet(sents[-1])))
        prev = ''
        starts = []
        for s in sents:
            if any(s.startswith(o) for o in FORMAL_OPENERS):
                res['formal_openers'].append((pi, s.split()[0], snippet(s)))
            for g in GENERIC_FRAMES:
                if re.search(g, s, re.I):
                    res['generic_frames'].append((pi, 'frame', snippet(s)))
                    break
            if PARTICIPIAL.search(s):
                res['participial_tails'].append((pi, PARTICIPIAL.search(s).group(1), snippet(s)))
            if NOT_ONLY.search(s):
                res['not_only_but_also'].append((pi, 'pattern', snippet(s)))
            if VAGUE.search(s):
                res['vague_quantifiers'].append((pi, VAGUE.search(s).group(1), snippet(s)))
            if SIGNIF.search(s) and not STAT_CUES.search(s):
                res['significant_without_stats'].append((pi, 'significant', snippet(s)))
            if COMPARATIVE.search(s) and not COMPARE_REF.search(s):
                res['comparison_without_referent'].append((pi, COMPARATIVE.search(s).group(1), snippet(s)))
            if HEDGE_STACK.search(s):
                res['hedge_stacks'].append((pi, 'hedge', snippet(s)))
            if VAGUE_START.match(s):
                res['ambiguous_sentence_starts'].append((pi, s.split()[0], 'prev: ' + snippet(prev, 70) + ' || ' + snippet(s, 70)))
            if len(s.split()) > 45:
                res['long_sentences'].append((pi, '%d words' % len(s.split()), snippet(s, 110)))
            starts.append(s.split()[0].lower() if s.split() else '')
            prev = s
        run = 1
        for i in range(1, len(starts)):
            run = run + 1 if starts[i] == starts[i - 1] and starts[i] else 1
            if run == 3:
                res['repeated_openers'].append((pi, starts[i], '3+ consecutive sentences start with "%s"' % starts[i]))

        # Advisory only: repeated determiner/possessive openings can create a list-like
        # cadence even when the literal first word changes. It is not a detector predictor.
        opener_family = re.compile(r'^(?:the|this|these|our|each)\b', re.I)
        family_hits = [s for s in sents if opener_family.search(s.strip())]
        if len(sents) >= 4 and len(family_hits) / len(sents) > 0.5:
            examples = ' | '.join(snippet(x, 75) for x in family_hits[:3])
            res['repetitive_opening_family'].append((pi, '%d/%d' % (len(family_hits), len(sents)), examples))

        # Similar lengths alone do not mean prose is bad. This advisory is emitted only
        # when sentence lengths cluster tightly AND the opening family is repetitive.
        lengths = [len(s.split()) for s in sents]
        if len(sents) >= 4 and family_hits and len(family_hits) / len(sents) > 0.5:
            median_len = statistics.median(lengths)
            near_median = sum(1 for n in lengths if abs(n - median_len) <= 3)
            if near_median / len(lengths) >= 0.75:
                res['flat_cadence'].append((pi, '%d/%d within +/-3 words of median' % (near_median, len(lengths)), 'Review whether the paragraph sounds list-like; do not force variation.'))

        # No connector is not an error. This low-confidence advisory asks whether the
        # logical relation is already clear from content. Never insert a connector just
        # to satisfy this heuristic.
        if len(sents) >= 4:
            relation = re.compile(r'\b(?:because|since|therefore|thus|as a result|consequently|however|in contrast|whereas|although|if|when|for example|specifically|in this setting|under this assumption)\b', re.I)
            if not any(relation.search(s) for s in sents[1:]):
                res['zero_explicit_relation_markers'].append((pi, 'no explicit relation marker', 'Check whether cause, contrast, condition, sequence, or evidence relations are still clear.'))
    low = text.lower()
    used = [w for w in SYNONYM_SET if re.search(r'\b' + w + r'\b', low)]
    if len(used) >= 3:
        res['term_cycling'].append((0, ', '.join(used), 'several near-synonyms in one text: check the terminology lock'))
    if len(pars) >= 4 and closers / len(pars) >= 0.4:
        info['notes'].append('%d of %d paragraphs end with a summary-style sentence.' % (closers, len(pars)))
    if len(pars) >= 4 and statistics.pstdev(sent_counts) == 0:
        info['notes'].append('All paragraphs have the same number of sentences (%d).' % sent_counts[0])
    return info, res


QUESTIONS = {
    'avoid_words': 'Is a plain, specific alternative available? Keep the word if it is a technical term, title, or quotation.',
    'formal_openers': 'Does the connector express a real relation, or is it decoration?',
    'summary_closers': 'Does the closing sentence add information, or repeat the paragraph?',
    'generic_frames': 'What concrete problem, result, or citation could open this sentence instead?',
    'participial_tails': 'What is the real consequence? Write it as its own clause or delete.',
    'not_only_but_also': 'State the facts plainly. Is the contrast real?',
    'vague_quantifiers': 'Does the project give the exact value? If not, keep an honest scope.',
    'significant_without_stats': 'Statistically significant (name the test) or merely large (give the number)?',
    'comparison_without_referent': 'Better than what, on which metric, by how much?',
    'hedge_stacks': 'Use one hedge that matches the evidence.',
    'ambiguous_sentence_starts': 'What exactly does the opening word refer to? Name it if two things could fit.',
    'repeated_openers': 'Do these sentences share a real structure, or is it a monotonous run?',
    'repetitive_opening_family': 'Several sentences begin with similar determiner/possessive patterns. Review as a group; do not force variety if the subject order is natural.',
    'flat_cadence': 'Sentence lengths are clustered alongside repetitive openings. Read aloud and revise only if the cadence impedes clarity.',
    'zero_explicit_relation_markers': 'Check whether logical relations are clear without explicit connectors; do not add a connector solely to satisfy this warning.',
    'long_sentences': 'Can condition and consequence be split along the logic?',
    'term_cycling': 'Are these one concept under different names?',
}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('file')
    ap.add_argument('--max', type=int, default=6, help='examples shown per category')
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()
    try:
        text = open(args.file, encoding='utf-8').read()
    except OSError as e:
        print('error: %s' % e, file=sys.stderr)
        return 2
    info, res = scan(text, args.file.lower().endswith(('.tex', '.sty')))
    if args.json:
        print(json.dumps({'info': info, 'findings': res, 'diagnostic_only': True, 'detector_prediction': False}, indent=2))
        return 0
    print('DIAGNOSTIC ONLY: hits are questions, not defects. Do not optimize toward zero hits.')
    print('Paragraphs: %d   Sentences: %d' % (info['paragraphs'], info['sentences']))
    for n in info['notes']:
        print('NOTE: ' + n)
    total = 0
    for cat, hits in res.items():
        if not hits:
            continue
        total += len(hits)
        print('\n[%s] %d hit(s)  ->  %s' % (cat, len(hits), QUESTIONS[cat]))
        for pi, tag, sn in hits[:args.max]:
            print('  p%d  %s: %s' % (pi, tag, sn))
        if len(hits) > args.max:
            print('  ... %d more' % (len(hits) - args.max))
    if total == 0:
        print('\nNo pattern hits. This does not show the text is clear or specific; run the reverse outline.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
