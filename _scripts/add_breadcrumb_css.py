#!/usr/bin/env python3
"""Add breadcrumb CSS to internal pages that got breadcrumb HTML but lack the styles."""
import os, glob

BASE = '/Users/edgarvernet/claude/alpeon'

PAGES = [
    'about/index.html', 'faq/index.html', 'contact/index.html', 'proprietaires/index.html',
    'en/about/index.html', 'en/faq/index.html', 'en/contact/index.html', 'en/proprietaires/index.html',
]

BC_CSS = """
  /* ── Breadcrumb ── */
  .breadcrumb { padding: .75rem 0; }
  .breadcrumb-list { display: flex; align-items: center; gap: .4rem; list-style: none; flex-wrap: wrap; }
  .breadcrumb-list li { display: flex; align-items: center; gap: .4rem; }
  .breadcrumb-list li::before { content: '›'; color: var(--mid, #4A5C4E); opacity: .4; font-size: .8rem; }
  .breadcrumb-list li:first-child::before { display: none; }
  .breadcrumb-list a { color: var(--mid, #4A5C4E); font-size: .72rem; letter-spacing: .06em; text-transform: uppercase; transition: color .2s; }
  .breadcrumb-list a:hover { color: var(--green, #2C3D30); }
  .breadcrumb-list span { color: var(--black, #111); font-size: .72rem; letter-spacing: .06em; text-transform: uppercase; opacity: .7; }
"""

done = 0
for relpath in PAGES:
    fp = f'{BASE}/{relpath}'
    if not os.path.exists(fp):
        continue
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    if '.breadcrumb-list {' in content:
        print(f'  SKIP (CSS already present): {relpath}')
        continue
    # Insert before </style>
    if '</style>' in content:
        content = content.replace('</style>', BC_CSS + '\n  </style>', 1)
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content)
        done += 1
        print(f'  OK: {relpath}')
    else:
        print(f'  WARN: no </style> tag in {relpath}')

print(f'\nDone: {done} pages updated')
