#!/usr/bin/env python3
"""Check explicitly mapped manuscript metrics against authoritative CSV values.

Usage:
    python scripts/metric_consistency.py --root PROJECT_ROOT --manifest writing-support/metric-audit.csv

The manifest maps each checked claim to one exact CSV row (by column filters), a
value column, and one or both manuscript locations: a paragraph anchor and/or a
LaTeX table label. It does not guess which arbitrary prose number means which metric.
Exit codes: 0 all mappings pass; 1 mismatch or invalid mapping; 2 usage/I/O error.
Python 3.8+, standard library only.
"""
import argparse
import csv
import re
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path

REQUIRED = {
    'claim_id', 'source_csv', 'source_value_column', 'source_filters',
    'manuscript_file', 'prose_anchor', 'table_label', 'table_row_anchor', 'unit', 'notes'
}
NUMBER_RE = re.compile(r'(?<![\w.])[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?%?(?![\w.])')
TABLE_RE = re.compile(r'\\begin\{(table\*?|longtable)\}.*?\\end\{\1\}', re.S)


def resolve_under_root(root, value):
    """Resolve a manifest path and reject traversal/symlinks outside project root."""
    path = Path(value)
    resolved = (path if path.is_absolute() else root / path).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError:
        raise ValueError('manifest paths must resolve inside the project root')
    return resolved


def parse_filters(blob):
    filters = {}
    for part in (blob or '').split(';'):
        part = part.strip()
        if not part:
            continue
        if '=' not in part:
            raise ValueError('Each source_filters item must be column=value')
        k, v = part.split('=', 1)
        filters[k.strip()] = v.strip()
    if not filters:
        raise ValueError('source_filters must identify exactly one source CSV row')
    return filters


def parse_numeric(value):
    value = str(value).strip().replace(',', '')
    if value.endswith('%'):
        value = value[:-1].strip()
    try:
        return Decimal(value)
    except (InvalidOperation, ValueError):
        return None


def numbers_in(text):
    return [n for n in (parse_numeric(m.group(0)) for m in NUMBER_RE.finditer(text)) if n is not None]


def paragraphs_for_anchor(text, anchor):
    """Return blank-line-delimited paragraphs containing the exact anchor."""
    if not anchor:
        return []
    return [paragraph for paragraph in re.split(r'\n\s*\n', text) if anchor in paragraph]


def sentences_for_anchor(paragraph, anchor):
    """Return sentences containing the anchor, with a conservative punctuation split."""
    # Decimal points do not split numbers because the following character is not whitespace.
    # This simple splitter is intended for explicit metric claims, not general NLP.
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z0-9\\(\[])', paragraph.strip())
    return [sentence for sentence in sentences if anchor in sentence]


def table_rows_for_label(text, label):
    """Return rows for one uniquely labeled LaTeX table, or a diagnostic sentinel."""
    if not label:
        return None
    label_re = re.compile(r'\\label\s*\{\s*' + re.escape(label.strip()) + r'\s*\}')
    tabular_re = re.compile(r'\\begin\{(tabular\*?|longtable|tblr)\}.*?\\end\{\1\}', re.S)
    row_sep = re.compile(r'\\\\(?:\s*\[[^\]]+\])?')
    matched_tables = [m.group(0) for m in TABLE_RE.finditer(text) if label_re.search(m.group(0))]
    if not matched_tables:
        return None
    if len(matched_tables) != 1:
        return 'DUPLICATE_LABEL'
    block = matched_tables[0]
    tabular_blocks = [m.group(0) for m in tabular_re.finditer(block)]
    if not tabular_blocks:
        # Some table environments (for example, longtable) are themselves tabular.
        if re.search(r'\\begin\{longtable\}', block):
            tabular_blocks = [block]
        else:
            return []
    rows = []
    for tabular in tabular_blocks:
        body = re.sub(r'^.*?\\begin\{(?:tabular\*?|longtable|tblr)\}[^}]*\}', '', tabular, count=1, flags=re.S)
        body = re.sub(r'\\end\{(?:tabular\*?|longtable|tblr)\}.*$', '', body, count=1, flags=re.S)
        rows.extend(row.strip() for row in row_sep.split(body) if row.strip())
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', default='.', help='project root; relative manifest paths resolve here')
    ap.add_argument('--manifest', required=True, help='CSV manifest path, absolute or relative to project root')
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        print('error: project root is not a directory', file=sys.stderr)
        return 2
    try:
        manifest_path = resolve_under_root(root, args.manifest)
    except ValueError as exc:
        print('error: invalid manifest path (%s)' % exc, file=sys.stderr)
        return 2
    try:
        with manifest_path.open('r', encoding='utf-8-sig', newline='') as f:
            reader = csv.DictReader(f)
            fields = set(reader.fieldnames or [])
            missing = sorted(REQUIRED - fields)
            if missing:
                print('error: manifest missing columns: ' + ', '.join(missing), file=sys.stderr)
                return 2
            mappings = [r for r in reader if any((v or '').strip() for v in r.values())]
    except OSError as exc:
        print('error: cannot read manifest (%s)' % exc, file=sys.stderr)
        return 2

    if not mappings:
        print('error: manifest has no claim mappings', file=sys.stderr)
        return 2

    outcomes = []
    fatal_io = False
    for idx, row in enumerate(mappings, 2):
        claim_id = (row.get('claim_id') or '').strip() or 'row-%d' % idx
        try:
            filters = parse_filters(row.get('source_filters', ''))
            source_path = resolve_under_root(root, (row.get('source_csv') or '').strip())
            manuscript_path = resolve_under_root(root, (row.get('manuscript_file') or '').strip())
            value_column = (row.get('source_value_column') or '').strip()
            anchor = (row.get('prose_anchor') or '').strip()
            label = (row.get('table_label') or '').strip()
            row_anchor = (row.get('table_row_anchor') or '').strip()
            if label and not row_anchor:
                raise ValueError('table_row_anchor is required when table_label is set')
            if not anchor and not label:
                raise ValueError('provide prose_anchor, table_label, or both')
            with source_path.open('r', encoding='utf-8-sig', newline='') as f:
                reader = csv.DictReader(f)
                headers = set(reader.fieldnames or [])
                missing_cols = (set(filters) | {value_column}) - headers
                if missing_cols:
                    raise ValueError('source CSV missing columns: ' + ', '.join(sorted(missing_cols)))
                matching = [r for r in reader if all((r.get(k) or '').strip().casefold() == v.casefold() for k, v in filters.items())]
            if len(matching) != 1:
                raise ValueError('source filters matched %d rows; exactly one is required' % len(matching))
            expected = parse_numeric(matching[0].get(value_column, ''))
            if expected is None:
                raise ValueError('source value is not a supported numeric scalar')
            manuscript_text = manuscript_path.read_text(encoding='utf-8')
            if manuscript_path.suffix.lower() in {'.tex', '.sty', '.cls'}:
                manuscript_text = re.sub(r'(?<!\\)%[^\n]*', '', manuscript_text)
            checked = []
            problems = []
            if anchor:
                paragraphs = paragraphs_for_anchor(manuscript_text, anchor)
                if not paragraphs:
                    problems.append('prose anchor not found')
                elif len(paragraphs) != 1 or paragraphs[0].count(anchor) != 1:
                    problems.append('prose_anchor must occur exactly once in one paragraph')
                else:
                    sentences = sentences_for_anchor(paragraphs[0], anchor)
                    if len(sentences) != 1:
                        problems.append('prose_anchor must identify exactly one sentence')
                    elif expected not in numbers_in(sentences[0]):
                        problems.append('source value absent from sentence matched by prose_anchor')
                    else:
                        checked.append('prose')
            if label:
                rows = table_rows_for_label(manuscript_text, label)
                if rows == 'DUPLICATE_LABEL':
                    problems.append('table label occurs in multiple table environments: ' + label)
                elif rows is None:
                    problems.append('LaTeX table label not found inside a table environment')
                elif rows == []:
                    problems.append('no supported tabular rows found for table ' + label)
                else:
                    matches = [row for row in rows if row_anchor in row]
                    if len(matches) != 1:
                        problems.append('table_row_anchor matched %d rows; exactly one is required' % len(matches))
                    elif expected not in numbers_in(matches[0]):
                        problems.append('source value absent from the row matched by table_row_anchor in ' + label)
                    else:
                        checked.append('table ' + label + ' row')
            if problems:
                outcomes.append({'claim_id': claim_id, 'status': 'FAIL', 'value': str(expected), 'checked': checked, 'problems': problems})
            else:
                outcomes.append({'claim_id': claim_id, 'status': 'PASS', 'value': str(expected), 'checked': checked, 'problems': []})
        except (OSError, ValueError, csv.Error) as exc:
            fatal_io = fatal_io or isinstance(exc, OSError)
            outcomes.append({'claim_id': claim_id, 'status': 'ERROR', 'value': None, 'checked': [], 'problems': [str(exc)]})

    if args.json:
        import json
        print(json.dumps({'manifest': str(manifest_path), 'outcomes': outcomes, 'ok': all(o['status'] == 'PASS' for o in outcomes)}, indent=2))
    else:
        print('METRIC CONSISTENCY AUDIT: explicit mappings only; not a scan of every number in the manuscript.')
        for item in outcomes:
            target = ', '.join(item['checked']) or 'no location verified'
            print('%s  %s  value=%s  locations=%s' % (item['status'], item['claim_id'], item['value'] or '-', target))
            for problem in item['problems']:
                print('  - ' + problem)
        passed = sum(1 for o in outcomes if o['status'] == 'PASS')
        print('Summary: %d/%d mappings passed.' % (passed, len(outcomes)))
    if fatal_io:
        return 2
    return 0 if all(o['status'] == 'PASS' for o in outcomes) else 1


if __name__ == '__main__':
    sys.exit(main())
