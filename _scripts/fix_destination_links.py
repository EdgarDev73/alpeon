#!/usr/bin/env python3
"""
Fix destination links across all HTML pages:
1. Footer links: all 6 point to /destinations/ → individual URLs
2. Home tiles: <a class="dest-card dc-*" href="/destinations/"> → individual URLs
"""
import os, glob

BASE = '/Users/edgarvernet/claude/alpeon'
ALL_HTML = glob.glob(f'{BASE}/**/*.html', recursive=True)

CITY_MAP = {
    'Courchevel':  'courchevel',
    'Megève':      'megeve',
    'Méribel':     'meribel',
    'Tignes':      'tignes',
    "Val d'Isère": 'val-d-isere',
    'Val Thorens': 'val-thorens',
}

TILE_MAP = {
    'dc-courchevel': 'courchevel',
    'dc-megeve':     'megeve',
    'dc-meribel':    'meribel',
    'dc-tignes':     'tignes',
    'dc-valdisere':  'val-d-isere',
    'dc-valthorens': 'val-thorens',
}

fixed_footer = 0
fixed_tiles  = 0

for filepath in sorted(ALL_HTML):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    rel = filepath.replace(BASE, '')
    is_en = rel.startswith('/en/')
    prefix = '/en' if is_en else ''
    changed = False

    # ── 1. Footer links ──
    for city, slug in CITY_MAP.items():
        new_href = f'{prefix}/destinations/{slug}/'
        # FR pages: href="/destinations/", EN pages: href="/en/destinations/"
        for old_href in ['/destinations/', '/en/destinations/']:
            old = f'href="{old_href}">{city}</a>'
            new = f'href="{new_href}">{city}</a>'
            if old in content:
                content = content.replace(old, new)
                fixed_footer += 1
                changed = True

    # ── 2. Home destination tiles ──
    for cls, slug in TILE_MAP.items():
        new_href = f'{prefix}/destinations/{slug}/'
        old = f'class="dest-card {cls}" href="/destinations/"'
        new = f'class="dest-card {cls}" href="{new_href}"'
        if old in content:
            content = content.replace(old, new)
            fixed_tiles += 1
            changed = True

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  OK: {rel}')

print(f'\nDone: {fixed_footer} footer links, {fixed_tiles} home tiles fixed')
