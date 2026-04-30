#!/usr/bin/env python3
"""
Add mobile globe/language toggle button to all pages.
Inserts:
  1. CSS <style> block before </head>
  2. .hdr-lang-wrap HTML before <div class="site-lang">
  3. JS <script> before </body>
"""

import os, glob, re

BASE = '/Users/edgarvernet/claude/alpeon'

# All HTML files that have hdr-phone-wrap (the mobile header)
all_files = glob.glob(f'{BASE}/**/index.html', recursive=True)
target_files = [f for f in all_files if 'node_modules' not in f]

LANG_CSS = """  <style>
  /* ── Header lang dropdown (mobile globe) ── */
  .hdr-lang-wrap { position: relative; display: none; }
  @media (max-width: 900px) { .hdr-lang-wrap { display: flex; align-items: center; } }
  .hdr-lang-btn {
    display: flex; align-items: center;
    background: none; border: none;
    padding: .35rem;
    color: rgba(232,203,160,.55); cursor: pointer;
    transition: color .2s; flex-shrink: 0;
  }
  .hdr-lang-btn:hover { color: var(--gold,#E8CBA0); }
  .hdr-lang-btn svg { width: 17px; height: 17px; stroke: currentColor; fill: none; stroke-width: 1.75; flex-shrink: 0; }
  .hdr-lang-dropdown {
    display: none; position: absolute; top: calc(100% + 6px); right: 0;
    background: #1a2a1e; border: 1px solid rgba(232,203,160,.15);
    border-radius: 8px; min-width: 110px; overflow: hidden;
    box-shadow: 0 16px 48px rgba(0,0,0,.45); z-index: 900;
  }
  .hdr-lang-wrap.open .hdr-lang-dropdown { display: block; }
  .hdr-lang-item {
    display: flex; align-items: center; gap: 8px;
    padding: 11px 16px; color: rgba(250,254,255,.75);
    font-size: .78rem; letter-spacing: .08em; text-transform: uppercase;
    transition: background .2s; text-decoration: none; white-space: nowrap;
  }
  .hdr-lang-item:hover { background: rgba(232,203,160,.08); color: var(--gold,#E8CBA0); }
  .hdr-lang-item.active { color: #C9A97A; }
  .hdr-lang-item + .hdr-lang-item { border-top: 1px solid rgba(250,254,255,.07); }
  </style>
</head>"""

LANG_HTML = """      <div class="hdr-lang-wrap" id="hdr-lang-wrap">
        <button class="hdr-lang-btn" onclick="toggleLangDropdown()" aria-label="Changer de langue">
          <svg viewBox="0 0 24 24" stroke="currentColor" fill="none" stroke-width="1.75"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
        </button>
        <div class="hdr-lang-dropdown" id="hdr-lang-dropdown"></div>
      </div>
      <div class="site-lang">"""

LANG_JS = """  <script>
  (function(){
    var wrap = document.getElementById('hdr-lang-wrap');
    var drop = document.getElementById('hdr-lang-dropdown');
    if(!wrap || !drop) return;
    // Build items from .site-lang links (hidden on mobile but still in DOM)
    var links = document.querySelectorAll('.site-lang a');
    links.forEach(function(a){
      var item = document.createElement('a');
      item.href = a.href;
      item.className = 'hdr-lang-item' + (a.classList.contains('active') ? ' active' : '');
      item.textContent = a.textContent.trim();
      drop.appendChild(item);
    });
    // Close on outside click
    document.addEventListener('click', function(e){
      if(!wrap.contains(e.target)) wrap.classList.remove('open');
    });
  })();
  function toggleLangDropdown(){
    var wrap = document.getElementById('hdr-lang-wrap');
    if(!wrap) return;
    // Close phone dropdown if open
    var phones = document.querySelectorAll('.hdr-phone-wrap.open');
    phones.forEach(function(el){ el.classList.remove('open'); });
    wrap.classList.toggle('open');
  }
  </script>
</body>"""

done = 0
skipped = 0
no_lang = 0

for filepath in sorted(target_files):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip files without hdr-phone-wrap (no mobile header)
    if 'hdr-phone-wrap' not in content:
        no_lang += 1
        continue

    # Skip if already processed
    if 'hdr-lang-wrap' in content:
        skipped += 1
        print(f'  SKIP (already done): {filepath.replace(BASE, "")}')
        continue

    # Skip if no site-lang (can't populate dropdown)
    if 'class="site-lang"' not in content:
        no_lang += 1
        print(f'  SKIP (no site-lang): {filepath.replace(BASE, "")}')
        continue

    # 1. Insert CSS <style> block before </head>
    if '</head>' not in content:
        print(f'  WARN (no </head>): {filepath.replace(BASE, "")}')
        continue
    content = content.replace('</head>', LANG_CSS, 1)

    # 2. Insert lang wrap HTML before <div class="site-lang">
    content = content.replace('<div class="site-lang">', LANG_HTML, 1)

    # 3. Insert JS before </body>
    content = content.replace('</body>', LANG_JS, 1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    done += 1
    print(f'  OK: {filepath.replace(BASE, "")}')

print(f'\nDone: {done} files modified, {skipped} skipped (already done), {no_lang} without mobile header')
