#!/usr/bin/env python3
"""
Add loyer-garanti to the footer Services column and link from accueil/proprietaires.
- FR pages: add <li><a href="/loyer-garanti/">Loyer garanti</a></li> after Estimateur de revenus
- EN pages: add <li><a href="/en/guaranteed-rent/">Guaranteed rent</a></li> after Revenue estimator
"""
import os, glob

BASE = '/Users/edgarvernet/claude/alpeon'

# Find all HTML files
all_html = glob.glob(f'{BASE}/**/*.html', recursive=True)
all_html = [f for f in all_html if '/_scripts/' not in f]

fr_added = 0
en_added = 0
skip = 0

for fp in sorted(all_html):
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()

    relpath = fp.replace(BASE + '/', '')
    is_en = relpath.startswith('en/')
    changed = False

    if is_en:
        # EN footer: add after Revenue estimator line
        old = '          <li><a href="/en/estimateur/">Revenue estimator</a></li>'
        new = old + '\n          <li><a href="/en/guaranteed-rent/">Guaranteed rent</a></li>'
        if old in content and '/en/guaranteed-rent/' not in content:
            content = content.replace(old, new, 1)
            changed = True
            en_added += 1
    else:
        # FR footer: add after Estimateur de revenus line
        old = '          <li><a href="/estimateur/">Estimateur de revenus</a></li>'
        new = old + '\n          <li><a href="/loyer-garanti/">Loyer garanti</a></li>'
        if old in content and 'href="/loyer-garanti/"' not in content:
            content = content.replace(old, new, 1)
            changed = True
            fr_added += 1

    if changed:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  OK: {relpath}')
    else:
        skip += 1

print(f'\nDone: {fr_added} FR + {en_added} EN pages updated, {skip} skipped')
