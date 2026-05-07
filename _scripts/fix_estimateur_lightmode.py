#!/usr/bin/env python3
"""
Replace the light mode override block in all estimateur pages.
Generates a comprehensive set of dark-text overrides for a white background.
"""

import os, glob, re

BASE = '/Users/edgarvernet/claude/alpeon'

PAGES = glob.glob(f'{BASE}/estimateur/*/index.html') + \
        glob.glob(f'{BASE}/en/estimateur/*/index.html') + \
        [f'{BASE}/estimateur/index.html']

# The new comprehensive light mode block
NEW_LIGHT_BLOCK = """  /* ═══ LIGHT MODE — fond blanc, textes sombres ═══ */

  /* ── Base ── */
  body { background: #faf9f7 !important; color: #1c1b19 !important; }

  /* ── Header (non scrollé : transparent sur fond blanc) ── */
  .site-nav-link { color: #2d2c2a !important; }
  .site-nav-link:hover { color: #2C3D30 !important; }
  .site-nav-lang, .site-nav-lang a { color: #7a7773 !important; }
  .site-lang, .site-lang a { color: #7a7773 !important; }
  .site-lang a.active { color: #C9A97A !important; }
  .site-burger span { background: rgba(28,27,25,.8) !important; }
  .site-header.scrolled { background: rgba(250,249,247,.97) !important; border-bottom-color: rgba(44,61,48,.12) !important; }
  .site-header.scrolled .site-nav-link { color: #2d2c2a !important; }

  /* ── Hero (garde le fond sombre pour le contraste — index uniquement) ── */
  .est-hero { background: var(--ink) !important; }
  .est-hero h1 { color: #fff !important; }
  .est-hero h1 em { color: var(--gold) !important; }
  .est-hero-eyebrow { color: var(--gold) !important; opacity: .85; }
  .est-hero-sub { color: rgba(250,254,255,.6) !important; }
  .est-hero-scroll { color: rgba(232,203,160,.5) !important; }

  /* Hero destination (pages station) */
  .dest-hero-content * { color: #fff !important; }
  .dest-hero-content em { color: var(--gold) !important; }

  /* ── Breadcrumb ── */
  .breadcrumb-list a { color: #7a7773 !important; }
  .breadcrumb-list li::before { color: #b0a89e !important; }
  .breadcrumb-list span { color: #4a4843 !important; }

  /* ── Barre stats ── */
  .dest-stats { background: #f2efe9 !important; border-bottom: 1px solid #e5dfd4; }
  .dest-stat-val { color: #2C3D30 !important; }
  .dest-stat-label { color: #7a7773 !important; }
  .dest-stat-sep { background: #d8d0c6 !important; }

  /* ── Trust bar ── */
  .trust-bar { background: #f2efe9 !important; border-color: #e5dfd4 !important; }
  .trust-label { color: #4a4843 !important; }
  .trust-icon { stroke: #2C3D30 !important; }
  .trust-sep { background: #d8d0c6 !important; }

  /* ── Titres & textes sections ── */
  .sec-eyebrow { color: #a8956a !important; }
  .sec-title { color: #1c1b19 !important; }
  .sec-title em { color: #a8956a !important; }
  .sec-desc, .sec-sub { color: #4a4843 !important; }

  /* ── Station cards ── */
  .st-card { background: #fff !important; border-color: #e5dfd4 !important; }
  .st-card:hover { border-color: #a8956a !important; box-shadow: 0 6px 24px rgba(0,0,0,.1) !important; }
  .st-card-name { color: #1c1b19 !important; }
  .st-card-sub { color: #7a7773 !important; }
  .st-card-range-label { color: #9a9390 !important; }
  .st-card-range-val { color: #2C3D30 !important; }
  .st-card-range-unit { color: #9a9390 !important; }
  .st-card-link { color: #2C3D30 !important; }
  .st-card-link svg { stroke: #2C3D30 !important; }
  .st-card-alt { color: #9a9390 !important; }

  /* ── How-it-works ── */
  .how-step { background: #fff !important; border-color: #e5dfd4 !important; }
  .how-step-num { color: rgba(44,61,48,.15) !important; }
  .how-step-title, .how-step h3 { color: #1c1b19 !important; }
  .how-step-desc, .how-step p { color: #4a4843 !important; }

  /* ── ALPÉON features ── */
  .feat-icon { background: rgba(44,61,48,.08) !important; }
  .feat-icon svg { stroke: #2C3D30 !important; }
  .feat-label { color: #4a4843 !important; }
  .feat-label strong { color: #1c1b19 !important; }
  .why-text p, .alpeon-features li { color: #4a4843 !important; }
  .why-num-val { color: #2C3D30 !important; }
  .why-num-label { color: #7a7773 !important; }
  .why-note { color: #9a9390 !important; }

  /* ── ALPÉON en chiffres ── */
  .alpeon-card { background: #fff !important; border: 1px solid #e5dfd4 !important; box-shadow: 0 2px 16px rgba(0,0,0,.06) !important; }
  .alpeon-card-title { color: #1c1b19 !important; border-bottom-color: #e5dfd4 !important; }
  .alpeon-num-val { color: #2C3D30 !important; }
  .alpeon-num-label { color: #7a7773 !important; }
  .alpeon-numbers { border-color: transparent !important; }

  /* ── Tableau revenus ── */
  .rev-table-wrap { border-color: #e5dfd4 !important; background: #fff !important; }
  .rev-table th { color: #7a7773 !important; border-bottom-color: #e5dfd4 !important; background: #f2efe9 !important; }
  .rev-table td { color: #1c1b19 !important; border-bottom-color: #f0ece6 !important; }
  .rev-table tr:hover td { background: #f8f5f0 !important; }
  .badge { background: #f2efe9 !important; color: #4a4843 !important; border-color: #e5dfd4 !important; }
  .badge-standing { background: #f2efe9 !important; color: #4a4843 !important; border-color: #e5dfd4 !important; }
  .badge-prestige { background: rgba(168,149,106,.12) !important; color: #8a7a56 !important; border-color: rgba(168,149,106,.3) !important; }
  .badge-luxe { background: #a8956a !important; color: #fff !important; }

  /* ── Résultats estimateur (pages station) ── */
  .res-title { color: #1c1b19 !important; }
  .res-sub { color: #4a4843 !important; }
  .res-range { color: #2C3D30 !important; }
  .res-card { background: #fff !important; border-color: #e5dfd4 !important; }
  .res-card-label { color: #7a7773 !important; }
  .res-card-val { color: #1c1b19 !important; }
  .step-label { color: #4a4843 !important; }
  .step-title { color: #1c1b19 !important; }
  .step-sub { color: #7a7773 !important; }
  .opt-label { color: #1c1b19 !important; }
  .opt-sub { color: #7a7773 !important; }
  .opt-card { background: #fff !important; border-color: #e5dfd4 !important; color: #1c1b19 !important; }
  .opt-card:hover { border-color: #a8956a !important; }
  .opt-card.selected { border-color: #2C3D30 !important; background: rgba(44,61,48,.05) !important; }

  /* ── FAQ ── */
  .faq-item { border-bottom-color: #e5dfd4 !important; }
  .faq-q { color: #1c1b19 !important; }
  .faq-q:hover { color: #2C3D30 !important; }
  .faq-icon { border-color: rgba(44,61,48,.25) !important; }
  .faq-icon svg { stroke: #4a4843 !important; }
  .faq-a { color: #4a4843 !important; }

  /* ── Autres stations / os-cards ── */
  .other-stations { background: #f2efe9 !important; border-top-color: #e5dfd4 !important; }
  .os-card { background: #fff !important; border: 1px solid #e5dfd4 !important; }
  .os-card-name { color: #1c1b19 !important; }
  .os-card-range { color: #7a7773 !important; }
  .os-card-link { color: #2C3D30 !important; }
  .os-card-link svg { stroke: #2C3D30 !important; }

  /* ── Sections ── */
  section.dest-section { background: #fff; }
  section.dest-section + section.dest-section { background: #f8f5f0; }
  section[style*="rgba(44,61,48"] { background: #f8f5f0 !important; }
  .stations, .how, .why, .faq-section, .alpeon-section { background: #faf9f7 !important; }

  /* ── CTA bas de page ── */
  .dest-cta { background: var(--green) !important; }
  .dest-cta-title { color: #fff !important; }
  .dest-cta-title em { color: var(--gold) !important; }
  .dest-cta-sub { color: rgba(250,254,255,.7) !important; }

  /* ── Newsletter inline ── */
  .nl-input { color: #1c1b19 !important; border-color: #d8d0c6 !important; background: #fff !important; }
  .nl-input::placeholder { color: #9a9390 !important; }
  .nl-label { color: #4a4843 !important; }
  .nl-note { color: #9a9390 !important; }
"""

OLD_BLOCK_START = '/* ═══ LIGHT MODE'

done = 0
for filepath in sorted(PAGES):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if OLD_BLOCK_START not in content:
        print(f'  SKIP (no light mode block): {filepath.replace(BASE, "")}')
        continue

    # Find the old light mode block and replace it
    # The block starts with /* ═══ LIGHT MODE and ends before </style>
    # Find the start
    start_idx = content.find(OLD_BLOCK_START)
    if start_idx == -1:
        continue

    # Find the enclosing </style> after the block
    end_idx = content.find('</style>', start_idx)
    if end_idx == -1:
        print(f'  WARN (no </style> after block): {filepath.replace(BASE, "")}')
        continue

    # Replace from start of block to the </style> (keep </style>)
    content = content[:start_idx] + NEW_LIGHT_BLOCK + '\n  </style>\n' + content[end_idx+8:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    done += 1
    print(f'  OK: {filepath.replace(BASE, "")}')

print(f'\nDone: {done} files updated')
