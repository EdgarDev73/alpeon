#!/usr/bin/env python3
"""
Add magazine to the footer Services column and header nav in all HTML files.
- FR pages: add <li><a href="/magazine/">Magazine</a></li> after Loyer garanti in footer
- EN pages: add <li><a href="/en/magazine/">Magazine</a></li> after Guaranteed rent in footer
"""
import os, glob

BASE = '/Users/edgarvernet/claude/alpeon'

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
        old = '          <li><a href="/en/guaranteed-rent/">Guaranteed rent</a></li>'
        new = old + '\n          <li><a href="/en/magazine/">Magazine</a></li>'
        # Also handle compact footer format (older EN dest pages)
        old2 = '        <li><a href="/en/guaranteed-rent/">Guaranteed rent</a></li>'
        new2 = old2 + '\n        <li><a href="/en/magazine/">Magazine</a></li>'
        if old in content and '/en/magazine/' not in content:
            content = content.replace(old, new, 1)
            changed = True
            en_added += 1
        elif old2 in content and '/en/magazine/' not in content:
            content = content.replace(old2, new2, 1)
            changed = True
            en_added += 1
    else:
        old = '          <li><a href="/loyer-garanti/">Loyer garanti</a></li>'
        new = old + '\n          <li><a href="/magazine/">Magazine</a></li>'
        if old in content and 'href="/magazine/"' not in content:
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
