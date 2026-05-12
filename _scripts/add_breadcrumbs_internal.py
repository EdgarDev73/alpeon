#!/usr/bin/env python3
"""
Add visible breadcrumb HTML nav to internal pages that have JSON-LD
BreadcrumbList but no visible breadcrumb element.

Pages: about, faq, contact, proprietaires (FR + EN)
"""
import os

BASE = '/Users/edgarvernet/claude/alpeon'

# (filepath, breadcrumb_items_html, insertion_anchor)
PAGES = [
    # FR
    ('about/index.html',
     '<!-- ═══ HERO ═══ -->\n<section class="page-hero">',
     [('Accueil', '/accueil/'), ('À propos', None)]),

    ('faq/index.html',
     None,  # will find dynamically
     [('Accueil', '/accueil/'), ('FAQ', None)]),

    ('contact/index.html',
     None,
     [('Accueil', '/accueil/'), ('Contact', None)]),

    ('proprietaires/index.html',
     None,
     [('Accueil', '/accueil/'), ('Propriétaires', None)]),

    # EN
    ('en/about/index.html',
     None,
     [('Home', '/en/accueil/'), ('About', None)]),

    ('en/faq/index.html',
     None,
     [('Home', '/en/accueil/'), ('FAQ', None)]),

    ('en/contact/index.html',
     None,
     [('Home', '/en/accueil/'), ('Contact', None)]),

    ('en/proprietaires/index.html',
     None,
     [('Home', '/en/accueil/'), ('Property Owners', None)]),
]

def make_breadcrumb(items, is_en=False):
    label = 'Breadcrumb' if is_en else "Fil d'Ariane"
    li_items = []
    for name, href in items:
        if href:
            li_items.append(f'    <li><a href="{href}">{name}</a></li>')
        else:
            li_items.append(f'    <li><span>{name}</span></li>')
    items_html = '\n'.join(li_items)
    return f'''<nav class="breadcrumb" aria-label="{label}" style="padding: .75rem var(--pad,2rem); max-width:var(--max,1380px); margin:0 auto;">
  <ol class="breadcrumb-list">
{items_html}
  </ol>
</nav>'''

def find_hero_anchor(content, filepath):
    """Find a consistent anchor to insert breadcrumb before."""
    candidates = [
        '<!-- ═══ HERO ═══ -->',
        '<section class="page-hero">',
        '<section class="hero',
        '<!-- ═══ PROPRIÉTAIRES',
        '<!-- ═══ FAQ',
        '<!-- ═══ CONTACT',
        '<main',
        '<section ',
    ]
    for c in candidates:
        if c in content:
            return c
    return None

done = 0
for relpath, anchor, items in PAGES:
    filepath = f'{BASE}/{relpath}'
    if not os.path.exists(filepath):
        print(f'  SKIP (not found): {relpath}')
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if breadcrumb nav already present
    if 'class="breadcrumb"' in content and '<nav' in content and 'breadcrumb-list' in content:
        # Check it's an actual nav element, not just CSS
        if '<nav class="breadcrumb"' in content:
            print(f'  SKIP (breadcrumb already present): {relpath}')
            continue

    is_en = relpath.startswith('en/')
    bc_html = make_breadcrumb(items, is_en)

    if anchor is None:
        anchor = find_hero_anchor(content, filepath)

    if anchor and anchor in content:
        content = content.replace(anchor, bc_html + '\n' + anchor, 1)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        done += 1
        print(f'  OK: {relpath}')
    else:
        print(f'  WARN: anchor not found in {relpath}')

print(f'\nDone: {done} pages updated')
