#!/usr/bin/env python3
"""Compare an original and an edited manuscript passage for integrity changes.

Usage:
    python integrity_check.py ORIGINAL EDITED [--ignore-numbers 3.8,4.1] [--json]

Checks (LaTeX, Markdown, or plain text; Python 3.8+, standard library only):
  CRITICAL  citation keys added or removed (\\cite family, [@key], numeric [12])
  CRITICAL  \\ref-family targets or \\label keys changed
  CRITICAL  math content changed (inline, display, equation/align environments)
  CRITICAL  numbers added or removed (counted as a multiset)
  CRITICAL  URLs or DOIs changed
  CRITICAL  \\begin/\\end environments or braces unbalanced in EDITED but balanced in ORIGINAL
  WARN      acronyms added or removed; large change in word count

Exit code: 0 no critical differences, 1 critical differences, 2 usage or file error.
A clean result does not prove the edit is correct; it only shows the mechanical items match.
"""
import utils.http_session
import utils.transport
import utils.session
import argparse
import json
import re
import sys
from collections import Counter

CITE_RE = re.compile(r'\\(?:[a-zA-Z]*cite[a-zA-Z]*|nocite)\*?(?:\[[^\]]*\])*\{([^}]*)\}')
REF_RE = re.compile(r'\\(?:[a-zA-Z]*ref|eqref|cref|Cref|autoref|pageref|nameref)\*?\{([^}]*)\}')
LABEL_RE = re.compile(r'\\label\{([^}]*)\}')
ENV_RE = re.compile(r'\\(begin|end)\{([^}]*)\}')
MATH_ENV_RE = re.compile(
    r'\\begin\{(equation\*?|align\*?|gather\*?|multline\*?|eqnarray\*?|displaymath|math)\}(.+?)\\end\{\1\}', re.S)
MATH_RES = [
    re.compile(r'\$\$(.+?)\$\$', re.S),
    re.compile(r'\\\[(.+?)\\\]', re.S),
    re.compile(r'\\\((.+?)\\\)', re.S),
    re.compile(r'(?<![\\$])\$(?!\$)(.+?)(?<![\\$])\$', re.S),
]
URL_RE = re.compile(r'https?://[^\s}\)\]>,;]+')
DOI_RE = re.compile(r'10\.\d{4,9}/[^\s}\)\]>,;]+')
MDCITE_RE = re.compile(r'\[@([^\]]+)\]')
NUMCIT_RE = re.compile(r'\[(\d+(?:\s*[,\u2013-]\s*\d+)*)\]')
NUM_RE = re.compile(r'(?<![\w.])[-+\u2212]?\d+(?:[.,]\d+)*(?:\s?%)?')
ACRO_RE = re.compile(r'\b[A-Z][A-Z0-9]{1,}(?:-[A-Z0-9]+)*\b')


def strip_comments(text):
    return re.sub(r'(?<!\\)%.*', '', text)


def split_keys(blob):
    return [k.strip() for k in blob.split(',') if k.strip()]


def extract(text):
    t = strip_comments(text)
    info = {}

    cites = Counter()
    for m in CITE_RE.finditer(t):
        cites.update(split_keys(m.group(1)))
    for m in MDCITE_RE.finditer(t):
        for k in re.split(r'[;,]', m.group(1)):
            k = k.strip().lstrip('@')
            if k:
                cites[k] += 1
    for m in NUMCIT_RE.finditer(t):
        for part in re.split(r'\s*,\s*', m.group(1)):
            cites['[' + part.strip() + ']'] += 1
    info['citations'] = cites

    info['refs'] = Counter(k for m in REF_RE.finditer(t) for k in split_keys(m.group(1)))
    info['labels'] = Counter(k for m in LABEL_RE.finditer(t) for k in split_keys(m.group(1)))

    math = Counter()
    rest = t
    for m in MATH_ENV_RE.finditer(t):
        math[re.sub(r'\s+', '', m.group(2))] += 1
    rest = MATH_ENV_RE.sub(' ', rest)
    for rx in MATH_RES:
        for m in rx.finditer(rest):
            math[re.sub(r'\s+', '', m.group(1))] += 1
        rest = rx.sub(' ', rest)
    info['math'] = math

    info['urls'] = Counter(u.rstrip('.') for u in URL_RE.findall(t))
    info['dois'] = Counter(d.rstrip('.') for d in DOI_RE.findall(t))

    # numbers: remove things that carry digits but are not prose numbers
    num_text = rest
    num_text = CITE_RE.sub(' ', num_text)
    num_text = REF_RE.sub(' ', num_text)
    num_text = LABEL_RE.sub(' ', num_text)
    num_text = URL_RE.sub(' ', num_text)
    num_text = DOI_RE.sub(' ', num_text)
    num_text = NUMCIT_RE.sub(' ', num_text)
    num_text = re.sub(r'\\[a-zA-Z]+\*?(?:\[[^\]]*\])?', ' ', num_text)
    nums = Counter()
    for m in NUM_RE.finditer(num_text):
        n = m.group(0).replace('\u2212', '-').replace(' ', '')
        nums[n.rstrip('.,')] += 1
    info['numbers'] = nums

    words = re.findall(r"[A-Za-z][A-Za-z'-]*", num_text)
    info['word_count'] = len(words)
    info['acronyms'] = Counter(ACRO_RE.findall(num_text))

    envs = Counter()
    for m in ENV_RE.finditer(t):
        envs[(m.group(1), m.group(2))] += 1
    info['env_unbalanced'] = sorted(
        {name for (_, name) in envs if envs[('begin', name)] != envs[('end', name)]})
    info['brace_balance'] = len(re.findall(r'(?<!\\)\{', t)) - len(re.findall(r'(?<!\\)\}', t))
    return info


def diff(a, b):
    removed = sorted((a - b).elements())
    added = sorted((b - a).elements())
    return removed, added


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('original')
    ap.add_argument('edited')
    ap.add_argument('--ignore-numbers', default='', help='comma-separated numbers the author approved changing')
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()

    try:
        a = open(args.original, encoding='utf-8').read()
        b = open(args.edited, encoding='utf-8').read()
    except OSError as e:
        print('error: %s' % e, file=sys.stderr)
        return 2

    ia, ib = extract(a), extract(b)
    ignore = {x.strip() for x in args.ignore_numbers.split(',') if x.strip()}
    critical, warn = [], []

    for key, label in [('citations', 'Citation keys'), ('refs', 'Cross-reference targets'),
                       ('labels', 'Labels'), ('math', 'Math content'),
                       ('urls', 'URLs'), ('dois', 'DOIs'), ('numbers', 'Numbers')]:
        rem, add = diff(ia[key], ib[key])
        if key == 'numbers':
            rem = [x for x in rem if x not in ignore]
            add = [x for x in add if x not in ignore]
        if rem or add:
            critical.append((label, rem, add))

    if ia['env_unbalanced'] == [] and ib['env_unbalanced']:
        critical.append(('Unbalanced environments in EDITED', ib['env_unbalanced'], []))
    if ia['brace_balance'] == 0 and ib['brace_balance'] != 0:
        critical.append(('Unbalanced braces in EDITED', ['balance=%d' % ib['brace_balance']], []))

    rem, add = diff(ia['acronyms'], ib['acronyms'])
    if rem or add:
        warn.append(('Acronyms', rem, add))
    wa, wb = ia['word_count'], ib['word_count']
    if wa and (wb < 0.7 * wa or wb > 1.4 * wa):
        warn.append(('Word count changed a lot', ['%d -> %d' % (wa, wb)], []))

    if args.json:
        print(json.dumps({'critical': critical, 'warnings': warn, 'ok': not critical}, indent=2))
    else:
        if not critical:
            print('OK: no critical mechanical differences (citations, refs, labels, math, numbers, URLs, DOIs).')
        for label, rem, add in critical:
            print('CRITICAL  %s' % label)
            if rem:
                print('   removed or changed from original: %s' % ', '.join(map(str, rem)))
            if add:
                print('   new in edited: %s' % ', '.join(map(str, add)))
        for label, rem, add in warn:
            print('WARN      %s' % label)
            if rem:
                print('   removed: %s' % ', '.join(map(str, rem)))
            if add:
                print('   added: %s' % ', '.join(map(str, add)))
        print('Words: %d -> %d' % (wa, wb))
    return 1 if critical else 0


if __name__ == '__main__':
    sys.exit(main())
