#!/usr/bin/env python3
"""Inventory a research project so an agent can read it efficiently.

Usage:
    python project_scan.py ROOT [--out FILE] [--max-files 5000]

Lists manuscripts, bibliographies, results and logs, code and config, data docs, figures,
notes, and candidate writing samples. For LaTeX it extracts the section outline and compares
cited keys with the .bib keys. Files that may contain secrets are listed but never read.
It does not execute any project code and does not modify the project.
Python 3.8+, standard library only.
"""
import argparse
import os
import re
import sys
import time

SKIP_DIRS = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 'env', '.idea', '.vscode', 'build', 'dist',
             '.ipynb_checkpoints', '.mypy_cache', '.pytest_cache', '.tox', 'site-packages', '.cache', 'writing-support'}
# Match credential-bearing filenames conservatively. Do not match arbitrary source
# names containing "token" (for example, tokenizer.py). Unknown files are never
# read merely because they are classified as a possible secret.
SECRET_EXACT_NAMES = {
    '.env', '.env.local', '.env.development', '.env.production', '.env.test', '.envrc',
    '.npmrc', '.pypirc', '.netrc', 'credentials', 'credential', 'secrets', 'secret',
    'token', 'tokens', 'access_token', 'refresh_token', 'api_token', 'api_key',
    'service-account.json', 'service_account.json', 'id_rsa', 'id_ed25519',
}
SECRET_SUFFIXES = ('.pem', '.key', '.p12', '.pfx', '.keystore', '.jks')
SECRET_STEM_RE = re.compile(
    r'(^|[._-])(?:credentials?|secrets?|api[_-]?keys?|access[_-]?tokens?|refresh[_-]?tokens?|client[_-]?secrets?|service[_-]?accounts?)([._-]|$)',
    re.I,
)

def is_sensitive_name(name):
    low = name.lower()
    stem, ext = os.path.splitext(low)
    if low == '.env' or low.startswith('.env.') or low == '.envrc' or low.startswith('.envrc.') or low in SECRET_EXACT_NAMES:
        return True
    if low.endswith(SECRET_SUFFIXES):
        return True
    if ext in {'.json', '.yaml', '.yml', '.toml', '.ini', '.conf', '.cfg', '.txt', '.env'} and SECRET_STEM_RE.search(stem):
        return True
    # Explicit access/API token names are protected only as whole filename stems.
    if stem in {'token', 'tokens', 'access_token', 'refresh_token', 'api_token', 'api_key'}:
        return True
    return False
CODE_EXT = {'.py', '.ipynb', '.r', '.jl', '.m', '.cpp', '.c', '.h', '.java', '.js', '.ts', '.sh', '.sql', '.rs', '.go'}
CONFIG_NAMES = {'requirements.txt', 'environment.yml', 'pyproject.toml', 'setup.py', 'dockerfile', 'makefile',
                'package.json', 'config.yaml', 'config.yml', 'config.json', 'conda.yml'}
IMG_EXT = {'.png', '.jpg', '.jpeg', '.svg', '.gif', '.eps', '.tiff', '.pdf'}
DATA_EXT = {'.csv', '.tsv', '.json', '.jsonl', '.parquet', '.xlsx', '.xls', '.log', '.txt', '.npy', '.pkl'}
RESULT_HINT = re.compile(r'result|metric|eval|score|report|ablation|benchmark|summary|log|stats', re.I)
ENTRY_HINT = re.compile(r'(train|eval|main|run|preprocess|prepare|infer|test|experiment)', re.I)


def human(n):
    for u in ('B', 'KB', 'MB', 'GB'):
        if n < 1024:
            return '%d%s' % (n, u) if u == 'B' else '%.1f%s' % (n, u)
        n /= 1024.0
    return '%.1fTB' % n


def read_text(path, limit=400000):
    # A project may contain symlinks to credentials or private data outside its root.
    # Inventory links by path/metadata only; never follow them for content.
    if os.path.islink(path):
        return ''
    try:
        with open(path, encoding='utf-8', errors='replace') as f:
            return f.read(limit)
    except OSError:
        return ''


def walk(root, max_files):
    files, skipped_dirs = [], []
    if max_files < 1:
        raise ValueError('--max-files must be at least 1')
    for dp, dns, fns in os.walk(root):
        keep = []
        for d in dns:
            (skipped_dirs if d in SKIP_DIRS else keep).append(os.path.join(dp, d) if d in SKIP_DIRS else d)
        dns[:] = keep
        for fn in fns:
            files.append(os.path.join(dp, fn))
            if len(files) > max_files:
                return files[:max_files], skipped_dirs, True
    return files, skipped_dirs, False


def bib_keys(text):
    return set(re.findall(r'@\w+\s*\{\s*([^,\s]+)\s*,', text))


def cite_keys(text):
    text = re.sub(r'(?<!\\)%.*', '', text)
    keys = set()
    for m in re.finditer(r'\\(?:[a-zA-Z]*cite[a-zA-Z]*)\*?(?:\[[^\]]*\])*\{([^}]*)\}', text):
        keys.update(k.strip() for k in m.group(1).split(',') if k.strip())
    return keys


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('root')
    ap.add_argument('--out')
    ap.add_argument('--max-files', type=int, default=5000)
    args = ap.parse_args()
    root = os.path.abspath(args.root)
    if not os.path.isdir(root):
        print('error: not a directory: %s' % root, file=sys.stderr)
        return 2

    try:
        files, skipped_dirs, truncated = walk(root, args.max_files)
    except ValueError as exc:
        print('error: %s' % exc, file=sys.stderr)
        return 2
    rel = lambda p: os.path.relpath(p, root)
    cats = {k: [] for k in ['manuscript', 'bib', 'results', 'code', 'config', 'data', 'figures', 'docs', 'office', 'secrets', 'other']}
    for p in files:
        name = os.path.basename(p)
        ext = os.path.splitext(name)[1].lower()
        try:
            size = os.path.getsize(p)
        except OSError:
            continue
        if is_sensitive_name(name):
            cats['secrets'].append((p, size))
            continue
        low = name.lower()
        if ext == '.bib':
            cats['bib'].append((p, size))
        elif low in CONFIG_NAMES:
            cats['config'].append((p, size))
        elif ext in CODE_EXT:
            cats['code'].append((p, size))
        elif ext in {'.docx', '.pptx', '.odt'}:
            cats['office'].append((p, size))
        elif ext in {'.tex', '.rst'} or (ext == '.md' and low not in ('readme.md',)) :
            cats['manuscript' if ext == '.tex' or 'paper' in p.lower() or 'draft' in low or 'thesis' in low else 'docs'].append((p, size))
        elif ext in IMG_EXT and (ext != '.pdf' or any(x in p.lower() for x in ('fig', 'plot', 'img', 'image'))):
            cats['figures'].append((p, size))
        elif ext == '.pdf':
            cats['manuscript'].append((p, size))
        elif ext in DATA_EXT:
            cats['results' if RESULT_HINT.search(name) or 'result' in p.lower() else 'data'].append((p, size))
        elif low == 'readme.md' or low.startswith('readme'):
            cats['docs'].append((p, size))
        else:
            cats['other'].append((p, size))

    out = []
    w = out.append
    w('# PROJECT_INVENTORY')
    w('')
    w('- Root: selected project directory (absolute path omitted for privacy)')
    w('- Symlink content is not opened; inspect link targets manually if they are trusted and needed.')
    w('- Scanned: %s' % time.strftime('%Y-%m-%d %H:%M'))
    w('- Files seen: %d%s' % (len(files), ' (stopped at --max-files; raise it or narrow ROOT)' if truncated else ''))
    w('- Skipped directories: %s' % (', '.join(sorted({os.path.basename(d) for d in skipped_dirs})) or 'none'))
    w('')
    w('## Counts')
    for k, v in cats.items():
        w('- %s: %d' % (k, len(v)))
    w('')

    # README paths only. Do not copy arbitrary project prose into the inventory;
    # the agent should open trusted documentation directly when needed.
    readmes = [p for p, _ in cats['docs'] if os.path.basename(p).lower().startswith('readme')]
    if readmes:
        w('## README files (paths only; content not copied)')
        for p, size in [item for item in cats['docs'] if item[0] in readmes][:10]:
            w('- `%s` (%s)' % (rel(p), human(size)))
        w('')

    # TeX outline and citations
    tex = [p for p, _ in cats['manuscript'] if p.lower().endswith('.tex')]
    if tex:
        w('## LaTeX manuscript')
        mains = [p for p in tex if r'\documentclass' in read_text(p, 20000)]
        w('- Main file(s): %s' % (', '.join('`%s`' % rel(p) for p in mains) or 'not found'))
        used = set()
        for p in tex:
            t = read_text(p)
            used |= cite_keys(t)
            heads = re.findall(r'\\(section|subsection|subsubsection)\*?\{([^}]*)\}', t)
            if heads:
                w('- Outline of `%s`:' % rel(p))
                for lvl, title in heads[:60]:
                    w('    %s%s' % ('  ' * ['section', 'subsection', 'subsubsection'].index(lvl), title))
            ab = re.search(r'\\begin\{abstract\}(.+?)\\end\{abstract\}', t, re.S)
            if ab:
                w('- Abstract found in `%s` (%d words)' % (rel(p), len(ab.group(1).split())))
        defined = set()
        for p, _ in cats['bib']:
            defined |= bib_keys(read_text(p))
        if cats['bib']:
            w('- Bib entries: %d; cited keys: %d' % (len(defined), len(used)))
            miss = sorted(used - defined)
            unused = sorted(defined - used)
            w('- Cited but missing from .bib (%d): %s' % (len(miss), ', '.join(miss[:30]) or 'none'))
            w('- In .bib but never cited (%d): %s' % (len(unused), ', '.join(unused[:30]) or 'none'))
        w('')

    # Notebooks
    nbs = [p for p, _ in cats['code'] if p.lower().endswith('.ipynb')]
    if nbs:
        w('## Notebooks')
        for p in nbs[:15]:
            t = read_text(p, 2000000)
            w('- `%s`: %d code cells, %s outputs' % (rel(p), t.count('"cell_type": "code"'), 'has' if '"outputs": [\n' in t or '"output_type"' in t else 'no'))
        w('')

    # Results candidates
    res = sorted(cats['results'], key=lambda x: x[0])
    if res:
        w('## Result and log candidates (check these for the real numbers)')
        for p, s in res[:40]:
            # Metadata only: never copy raw result rows, logs, or participant-level data
            # into an inventory that may be passed to an external LLM.
            w('- `%s` (%s; content not previewed)' % (rel(p), human(s)))
        if len(res) > 40:
            w('- ... %d more' % (len(res) - 40))
        w('')

    # Code entry points and config
    code = cats['code']
    if code:
        w('## Code')
        entries = [p for p, _ in code if ENTRY_HINT.search(os.path.basename(p))]
        w('- Source files: %d; likely entry points: %s' % (len(code), ', '.join('`%s`' % rel(p) for p in entries[:20]) or 'none found'))
        w('- Code paths (first 60, filenames only): %s' % (', '.join('`%s`' % rel(p) for p, _ in code[:60]) or 'none'))
        if len(code) > 60:
            w('- ... %d additional source paths not shown' % (len(code) - 60))
    if cats['config']:
        w('- Config and environment: %s' % ', '.join('`%s`' % rel(p) for p, _ in cats['config'][:20]))
    if code or cats['config']:
        w('- Reminder: config is not proof of what was run; confirm settings against logs.')
        w('')

    # Data docs
    if cats['data']:
        w('## Data files (do not paste private records; describe schema only)')
        by_dir = {}
        for p, s in cats['data']:
            by_dir.setdefault(os.path.dirname(rel(p)) or '.', []).append((p, s))
        for d, items in sorted(by_dir.items())[:25]:
            w('- `%s/`: %d file(s), %s' % (d, len(items), human(sum(s for _, s in items))))
        w('')

    # Figures
    if cats['figures']:
        by_dir = {}
        for p, _ in cats['figures']:
            by_dir.setdefault(os.path.dirname(rel(p)) or '.', []).append(os.path.basename(p))
        w('## Figures')
        for d, names in sorted(by_dir.items())[:15]:
            w('- `%s/`: %d file(s), e.g. %s' % (d, len(names), ', '.join(sorted(names)[:5])))
        w('')

    # Notes and docs
    others = [p for p, _ in cats['docs'] if p not in readmes]
    if others:
        w('## Notes and documents (paths only; content not copied)')
        for p, size in [item for item in cats['docs'] if item[0] in others][:30]:
            w('- `%s` (%s)' % (rel(p), human(size)))
        w('')

    if cats['office']:
        w('## Office files (extract text with your tool before reading)')
        for p, s in cats['office'][:20]:
            w('- `%s` (%s)' % (rel(p), human(s)))
        w('')

    # Writing sample candidates
    cand = [p for p, _ in cats['manuscript'] + cats['docs'] + cats['office'] if p not in readmes]
    if cand:
        w('## Candidate writing samples for the voice profile')
        w('Provenance is UNKNOWN for all of these. Use only text the author wrote; ask which files those are, and exclude AI-written or third-party text.')
        for p in cand[:30]:
            wc = len(read_text(p).split()) if p.lower().endswith(('.tex', '.md', '.txt', '.rst')) else 0
            when = time.strftime('%Y-%m-%d', time.localtime(os.path.getmtime(p)))
            w('- `%s` (%s%s)' % (rel(p), ('%d words, ' % wc) if wc else '', 'modified ' + when))
        w('')

    if cats['secrets']:
        w('## Possible secrets (listed, NOT read)')
        for p, s in cats['secrets']:
            w('- `%s`' % rel(p))
        w('')

    w('## Next steps for the agent')
    w('1. Read trusted project documentation directly; use this inventory for paths and structure only.')
    w('2. Read result files directly only when needed and permitted; inspect schemas first and never copy private rows into summaries.')
    w('3. Fill `templates/project-brief.md` with source pointers; list conflicts and open questions.')
    w('4. Build `templates/voice-profile.md` from author-written samples only.')
    text = '\n'.join(out) + '\n'
    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)) or '.', exist_ok=True)
        with open(args.out, 'w', encoding='utf-8') as f:
            f.write(text)
        print('Wrote project inventory (%d lines; output path omitted)' % len(out))
    else:
        sys.stdout.write(text)
    return 0


if __name__ == '__main__':
    sys.exit(main())
