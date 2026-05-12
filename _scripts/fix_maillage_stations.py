#!/usr/bin/env python3
"""
Complete inter-station cross-links: each station page should link to all 5 others.
Currently each links to only 3. Adding the 2 missing ones per page.

Missing links per station:
  courchevel  : tignes, val-thorens
  megeve      : meribel, tignes
  meribel     : megeve, tignes
  tignes      : megeve, meribel
  val-d-isere : megeve, val-thorens
  val-thorens : megeve, val-d-isere
"""
import os

BASE = '/Users/edgarvernet/claude/alpeon'

STATIONS = {
    'courchevel': {
        'fr_name': 'Courchevel', 'en_name': 'Courchevel',
        'massif': 'Les 3 Vallées',
    },
    'megeve': {
        'fr_name': 'Megève', 'en_name': 'Megève',
        'massif': 'Mont-Blanc',
    },
    'meribel': {
        'fr_name': 'Méribel', 'en_name': 'Méribel',
        'massif': 'Les 3 Vallées',
    },
    'tignes': {
        'fr_name': 'Tignes', 'en_name': 'Tignes',
        'massif': 'Espace Killy',
    },
    'val-d-isere': {
        'fr_name': "Val d'Isère", 'en_name': "Val d'Isère",
        'massif': 'Espace Killy',
    },
    'val-thorens': {
        'fr_name': 'Val Thorens', 'en_name': 'Val Thorens',
        'massif': 'Les 3 Vallées',
    },
}

MISSING = {
    'courchevel':  ['tignes', 'val-thorens'],
    'megeve':      ['meribel', 'tignes'],
    'meribel':     ['megeve', 'tignes'],
    'tignes':      ['megeve', 'meribel'],
    'val-d-isere': ['megeve', 'val-thorens'],
    'val-thorens': ['megeve', 'val-d-isere'],
}

ANCHOR = '</div>\n    </div>\n  </div>\n</section>\n\n\n<!-- ── DÉCOUVREZ NOS BIENS'

def make_fr_card(slug, info):
    massif = info['massif']
    name = info['fr_name']
    return f'''      <a href="/destinations/{slug}/" class="maillage-card">
        <div class="maillage-cat">Station voisine · {massif}</div>
        <div class="maillage-label">Gestion locative à {name}</div>
        <div class="maillage-arrow">→</div>
      </a>'''

def make_en_card(slug, info):
    massif = info['massif']
    name = info['en_name']
    return f'''      <a href="/en/destinations/{slug}/" class="maillage-card">
        <div class="maillage-cat">Neighbouring resort · {massif}</div>
        <div class="maillage-label">Property management in {name}</div>
        <div class="maillage-arrow">→</div>
      </a>'''

done = 0
for station_slug, missing_slugs in MISSING.items():
    for lang in ['fr', 'en']:
        if lang == 'fr':
            filepath = f'{BASE}/destinations/{station_slug}/index.html'
        else:
            filepath = f'{BASE}/en/destinations/{station_slug}/index.html'

        if not os.path.exists(filepath):
            print(f'  WARN: {filepath} not found')
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find the maillage-grid closing tag and insert before it
        # The anchor is the last </a> before </div>\n    </div> of maillage-grid
        # We find </div>\n  </div>\n</section>\n\n\n<!-- ── DÉCOUVREZ NOS BIENS
        # and insert new cards just before the last </div> of .maillage-grid

        # Find the maillage section anchor
        grid_end = '</div>\n    </div>\n  </div>\n</section>'

        if grid_end not in content:
            # Try alternate spacing
            grid_end = '</div>\n      </div>\n    </div>\n  </div>\n</section>'

        # Better: find the maillage-grid div end
        # Insert new cards right before the closing </div> of maillage-grid
        marker = '      <a href="/destinations/" class="maillage-card">' if lang == 'fr' else '      <a href="/en/destinations/" class="maillage-card">'

        if marker not in content:
            print(f'  WARN: marker not found in {filepath.replace(BASE,"")}')
            continue

        new_cards = ''
        for slug in missing_slugs:
            info = STATIONS[slug]
            if lang == 'fr':
                new_cards += make_fr_card(slug, info) + '\n'
            else:
                new_cards += make_en_card(slug, info) + '\n'

        # Insert before the "Toutes nos destinations" card
        content = content.replace(marker, new_cards + marker, 1)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        done += 1
        print(f'  OK: {filepath.replace(BASE, "")}')

print(f'\nDone: {done} files updated')
