#!/usr/bin/env python3
"""
Fix loyer-garanti/index.html and en/guaranteed-rent/index.html:
1. Add missing footer CSS
2. Fix white section backgrounds
3. Adapt text colors for light sections
"""
import os, re

BASE = '/Users/edgarvernet/claude/alpeon'

# ── Extract footer CSS from proprietaires ──
with open(f'{BASE}/proprietaires/index.html', 'r', encoding='utf-8') as f:
    prop = f.read()

# Extract lines 636-707 of footer CSS (footer element + all footer classes)
footer_css_start = prop.find('\n    footer { background: #0d1410;')
footer_css_end = prop.find('\n/* @@LANG-DROPDOWN', footer_css_start)
if footer_css_end == -1:
    # fallback: find after the media queries
    footer_css_end = prop.find('\n\n\n', footer_css_start)
footer_css_block = prop[footer_css_start:footer_css_end].strip()

# Also grab footer-owner inline styles (they appear as inline <style> at bottom of prop)
footer_owner_css = """
  /* ── Footer owner CTA ── */
  .footer-owner-cta { border-top: none; padding: .85rem 0; }
  .footer-owner-flex { display: flex; align-items: center; justify-content: center; gap: .7rem; flex-wrap: wrap; }
  .footer-owner-sep { color: rgba(250,254,255,.18); font-size: .7rem; line-height: 1; }
  .footer-owner-text { color: rgba(250,254,255,.3); font-size: .72rem; font-family: var(--font-sans); font-weight: 300; letter-spacing: .03em; }
  .footer-owner-btn { display: inline-flex; align-items: center; gap: .3rem; color: rgba(232,203,160,.5); font-size: .72rem; font-family: var(--font-sans); font-weight: 400; letter-spacing: .03em; text-decoration: none; transition: color .2s; white-space: nowrap; }
  .footer-owner-btn:hover { color: #E8CBA0; }"""

# ── Patch a page ──
def patch_page(fp, is_en=False):
    with open(fp, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Add footer CSS before </style>
    if '.footer-grid {' not in html:
        footer_css_inject = f"""
  {footer_owner_css}

  /* ── Footer ── */
  footer {{ background: #0d1410; padding: 0; border-top: 1px solid rgba(232,203,160,.12); }}
  footer > .container {{ padding-top: clamp(48px,6vw,72px); }}
  .footer-grid {{
    display: grid;
    grid-template-columns: 2fr 1fr 1fr 1fr;
    gap: 48px;
    padding-bottom: 48px;
    border-bottom: 1px solid rgba(250,254,255,.07);
  }}
  .footer-brand-logo {{ margin-bottom: 14px; }}
  .footer-brand-claim {{
    font-size: .58rem; font-weight: 600; letter-spacing: .22em;
    text-transform: uppercase; color: var(--gold,#E8CBA0); margin-bottom: 16px; opacity: .85;
  }}
  .footer-brand-text {{
    font-size: .81rem; font-weight: 300;
    color: rgba(250,254,255,.32); line-height: 1.8; max-width: 270px;
  }}
  .footer-col-title {{
    font-size: .58rem; font-weight: 600; letter-spacing: .2em;
    text-transform: uppercase; color: rgba(250,254,255,.22); margin-bottom: 18px;
  }}
  .footer-links {{ list-style: none; display: flex; flex-direction: column; gap: 11px; }}
  .footer-links a {{
    font-size: .83rem; font-weight: 300;
    color: rgba(250,254,255,.48); transition: color .2s; text-decoration: none;
  }}
  .footer-links a:hover {{ color: var(--gold,#E8CBA0); }}
  .footer-lower {{
    display: grid;
    grid-template-columns: 1fr 2fr;
    gap: 48px;
    padding: 40px 0 48px;
    border-bottom: 1px solid rgba(250,254,255,.07);
  }}
  .footer-socials {{ display: flex; gap: 14px; align-items: center; margin-top: 4px; }}
  .footer-social-link {{
    display: flex; align-items: center; justify-content: center;
    width: 36px; height: 36px; border-radius: 50%;
    border: 1px solid rgba(250,254,255,.15);
    color: rgba(250,254,255,.48); transition: all .2s;
  }}
  .footer-social-link:hover {{ border-color: var(--gold,#E8CBA0); color: var(--gold,#E8CBA0); background: rgba(232,203,160,.07); }}
  .footer-social-link svg {{ width: 16px; height: 16px; fill: currentColor; }}
  .nl-form {{ display: flex; gap: 8px; margin-top: 4px; }}
  .nl-input {{
    flex: 1; border: 1px solid rgba(250,254,255,.12); border-radius: 4px;
    background: rgba(250,254,255,.05); color: #fff;
    padding: .55rem .85rem; font-size: .8rem; font-family: inherit; outline: none;
    transition: border-color .2s;
  }}
  .nl-input::placeholder {{ color: rgba(250,254,255,.25); }}
  .nl-input:focus {{ border-color: rgba(232,203,160,.45); }}
  .nl-btn {{
    background: var(--gold,#E8CBA0); color: #1a2a1e; border: none; border-radius: 4px;
    padding: .55rem 1.1rem; font-size: .72rem; font-weight: 700;
    letter-spacing: .1em; text-transform: uppercase; cursor: pointer;
    white-space: nowrap; transition: opacity .2s; font-family: inherit;
  }}
  .nl-btn:hover {{ opacity: .85; }}
  .nl-msg {{ font-size: .73rem; margin-top: .5rem; min-height: 1em; }}
  .nl-msg.ok {{ color: #86efac; }} .nl-msg.err {{ color: #fca5a5; }}
  .footer-bottom {{
    padding: 24px 0; display: flex;
    justify-content: space-between; align-items: center; gap: 12px;
  }}
  .footer-bottom span {{ font-size: .68rem; color: rgba(250,254,255,.18); }}
  @media(max-width:1024px){{ .footer-grid{{ grid-template-columns:1fr 1fr; gap:36px; }} .footer-lower{{ grid-template-columns:1fr; }} }}
  @media(max-width:600px){{ .footer-grid{{ grid-template-columns:1fr; }} .footer-bottom{{ flex-direction:column; text-align:center; }} }}
"""
        html = html.replace('  </style>', footer_css_inject + '\n  </style>', 1)

    # 2. White backgrounds — Steps section
    html = html.replace(
        '.lg-steps { background: rgba(44,61,48,.18); border-top: 1px solid rgba(232,203,160,.06); border-bottom: 1px solid rgba(232,203,160,.06); padding: 80px var(--pad); }',
        '.lg-steps { background: #fff; border-top: 1px solid #e8e4dd; border-bottom: 1px solid #e8e4dd; padding: 80px var(--pad); }'
    )
    # Step cards
    html = html.replace(
        '.lg-step { padding: 2rem; background: rgba(255,255,255,.04); border: 1px solid rgba(232,203,160,.12); border-radius: 12px; }',
        '.lg-step { padding: 2rem; background: #f7f5f1; border: 1px solid #e0dbd3; border-radius: 12px; }'
    )
    html = html.replace(
        '.lg-step-num { width: 44px; height: 44px; border: 1px solid rgba(232,203,160,.3); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-family: var(--font-serif); font-size: 1rem; color: var(--gold); margin-bottom: 1.25rem; }',
        '.lg-step-num { width: 44px; height: 44px; border: 1px solid rgba(168,149,106,.4); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-family: var(--font-serif); font-size: 1rem; color: #9c7d45; margin-bottom: 1.25rem; }'
    )
    html = html.replace(
        '.lg-step h3 { font-size: .95rem; font-weight: 500; color: rgba(250,254,255,.9); margin-bottom: .6rem; }',
        '.lg-step h3 { font-size: .95rem; font-weight: 500; color: #1a2a1e; margin-bottom: .6rem; }'
    )
    html = html.replace(
        '.lg-step p { font-size: .83rem; color: rgba(250,254,255,.45); line-height: 1.75; }',
        '.lg-step p { font-size: .83rem; color: rgba(30,45,35,.55); line-height: 1.75; }'
    )
    # Sec titles in white sections (steps)
    # We'll add dedicated classes in HTML; for now adjust via section-scoped override
    html = html.replace(
        '  /* Steps */\n  .lg-steps {',
        '  /* Steps */\n  .lg-steps .sec-eyebrow { color: #9c7d45; }\n  .lg-steps .sec-title { color: #1a2a1e; }\n  .lg-steps {'
    )

    # 3. White background — Compare section (inline style on section tag)
    html = html.replace(
        '<section style="background:rgba(44,61,48,.08); border-top:1px solid rgba(232,203,160,.06)">',
        '<section style="background:#fff; border-top:1px solid #e8e4dd">'
    )
    # Compare table text colors for white bg
    html = html.replace(
        '.lg-compare-table thead th { font-size: .72rem; letter-spacing: .12em; text-transform: uppercase; color: rgba(250,254,255,.4); font-weight: 400; }',
        '.lg-compare-table thead th { font-size: .72rem; letter-spacing: .12em; text-transform: uppercase; color: rgba(30,45,35,.4); font-weight: 400; }'
    )
    html = html.replace(
        '.lg-compare-table thead th:nth-child(2) { color: var(--gold); }',
        '.lg-compare-table thead th:nth-child(2) { color: #9c7d45; }'
    )
    html = html.replace(
        '.lg-compare-table td:nth-child(2) { color: rgba(250,254,255,.9); }',
        '.lg-compare-table td:nth-child(2) { color: #1a2a1e; }'
    )
    html = html.replace(
        '.lg-compare-table td:nth-child(1) { color: rgba(250,254,255,.6); }',
        '.lg-compare-table td:nth-child(1) { color: rgba(30,45,35,.65); }'
    )
    html = html.replace(
        '.lg-compare-table td:nth-child(3) { color: rgba(250,254,255,.35); }',
        '.lg-compare-table td:nth-child(3) { color: rgba(30,45,35,.38); }'
    )
    html = html.replace(
        '.lg-compare-table th, .lg-compare-table td { padding: 1rem 1.25rem; text-align: left; border-bottom: 1px solid rgba(232,203,160,.08); font-size: .85rem; }',
        '.lg-compare-table th, .lg-compare-table td { padding: 1rem 1.25rem; text-align: left; border-bottom: 1px solid #ece9e3; font-size: .85rem; }'
    )
    # Compare sec titles
    html = html.replace(
        '  /* Comparatif */\n  .lg-compare {',
        '  /* Comparatif */\n  .lg-compare .sec-eyebrow { color: #9c7d45; }\n  .lg-compare .sec-title { color: #1a2a1e; }\n  .lg-compare .sec-desc { color: rgba(30,45,35,.5); }\n  .lg-compare {'
    )

    # 4. White background — FAQ section
    html = html.replace(
        '<section style="background:rgba(44,61,48,.12)">',
        '<section style="background:#fff; border-top:1px solid #e8e4dd">'
    )
    html = html.replace(
        '.lg-faq h2 { font-family: var(--font-serif); font-size: clamp(1.6rem, 3.5vw, 2.2rem); color: #fff; margin-bottom: 2.5rem; }',
        '.lg-faq h2 { font-family: var(--font-serif); font-size: clamp(1.6rem, 3.5vw, 2.2rem); color: #1a2a1e; margin-bottom: 2.5rem; }'
    )
    html = html.replace(
        '.lg-faq h2 { font-family: var(--font-serif); font-size: clamp(1.6rem, 3.5vw, 2.2rem); color: #1a2a1e; margin-bottom: 2.5rem; }',
        '.lg-faq h2 { font-family: var(--font-serif); font-size: clamp(1.6rem, 3.5vw, 2.2rem); color: #1a2a1e; margin-bottom: 2.5rem; }'
    )
    # Fix the em color in faq h2 for white bg
    html = html.replace(
        '<h2>Questions fréquentes sur le <em style="font-style:italic;color:var(--gold)">loyer garanti</em></h2>',
        '<h2>Questions fréquentes sur le <em style="font-style:italic;color:#9c7d45">loyer garanti</em></h2>'
    )
    html = html.replace(
        '<h2>Frequently asked questions about <em style="font-style:italic;color:var(--gold)">guaranteed rent</em></h2>',
        '<h2>Frequently asked questions about <em style="font-style:italic;color:#9c7d45">guaranteed rent</em></h2>'
    )
    html = html.replace(
        '.faq-item { border-bottom: 1px solid rgba(232,203,160,.1); }',
        '.faq-item { border-bottom: 1px solid #e8e4dd; }'
    )
    html = html.replace(
        '.faq-q { width: 100%; background: none; border: none; text-align: left; padding: 1.25rem 0; cursor: pointer; display: flex; justify-content: space-between; align-items: center; gap: 1rem; color: rgba(250,254,255,.9); font-size: .92rem; font-family: var(--font-sans); font-weight: 400; line-height: 1.5; }',
        '.faq-q { width: 100%; background: none; border: none; text-align: left; padding: 1.25rem 0; cursor: pointer; display: flex; justify-content: space-between; align-items: center; gap: 1rem; color: #1a2a1e; font-size: .92rem; font-family: var(--font-sans); font-weight: 400; line-height: 1.5; }'
    )
    html = html.replace(
        '.faq-q:hover { color: #fff; }',
        '.faq-q:hover { color: #2C3D30; }'
    )
    html = html.replace(
        '.faq-icon { width: 28px; height: 28px; border: 1px solid rgba(232,203,160,.2); border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }',
        '.faq-icon { width: 28px; height: 28px; border: 1px solid rgba(44,61,48,.25); border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }'
    )
    html = html.replace(
        '.faq-icon svg { width: 12px; height: 12px; stroke: rgba(250,254,255,.6); transition: transform .25s; }',
        '.faq-icon svg { width: 12px; height: 12px; stroke: rgba(30,45,35,.55); transition: transform .25s; }'
    )
    html = html.replace(
        '.faq-a { display: none; padding: 0 0 1.25rem; color: rgba(250,254,255,.45); font-size: .85rem; line-height: 1.75; }',
        '.faq-a { display: none; padding: 0 0 1.25rem; color: rgba(30,45,35,.55); font-size: .85rem; line-height: 1.75; }'
    )

    return html


# ── FR ──
fp_fr = f'{BASE}/loyer-garanti/index.html'
html_fr = patch_page(fp_fr, is_en=False)
with open(fp_fr, 'w', encoding='utf-8') as f:
    f.write(html_fr)
print('Fixed: loyer-garanti/index.html')

# ── EN ──
fp_en = f'{BASE}/en/guaranteed-rent/index.html'
with open(fp_en, 'r', encoding='utf-8') as f:
    html_en = f.read()

# EN has same CSS classes but slightly different strings — apply same transforms
html_en = patch_page(fp_en, is_en=True)
with open(fp_en, 'w', encoding='utf-8') as f:
    f.write(html_en)
print('Fixed: en/guaranteed-rent/index.html')
