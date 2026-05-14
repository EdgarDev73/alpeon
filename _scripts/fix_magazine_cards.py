#!/usr/bin/env python3
"""Convert article cards from <article> to <a href="..."> in magazine/index.html"""
import re

CARDS_FR = [
    ("Investir à Courchevel", "investir-courchevel-2025"),
    ("Val d'Isère vs. Méribel", "val-d-isere-vs-meribel-rendement-locatif"),
    ("Neuf ou ancien en station", "neuf-vs-ancien-station-ski"),
    ("LMNP en 2025", "lmnp-2025-guide-complet"),
    ("Amortissement LMNP", "amortissement-lmnp-chalet"),
    ("Micro-BIC vs. régime réel", "micro-bic-vs-regime-reel"),
    ("Tignes", "tignes-saison-2024-2025"),
    ("Megève hors-saison", "megeve-demande-estivale"),
    ("Val Thorens en été", "val-thorens-ete-diversification"),
    ("ALPÉON coordonne", "alpeon-gestion-200-proprietes"),
    ("Tarification dynamique", "tarification-dynamique-revpar"),
    ("Loyer garanti vs. commission", "loyer-garanti-vs-commission"),
]

CARDS_EN = [
    ("Investing in Courchevel", "investir-courchevel-2025"),
    ("Val d'Isère vs. Méribel", "val-d-isere-vs-meribel-rendement-locatif"),
    ("New-build vs. resale", "neuf-vs-ancien-station-ski"),
    ("LMNP in 2025", "lmnp-2025-guide-complet"),
    ("LMNP depreciation", "amortissement-lmnp-chalet"),
    ("Micro-BIC vs. real regime", "micro-bic-vs-regime-reel"),
    ("Tignes", "tignes-saison-2024-2025"),
    ("Megève off-season", "megeve-demande-estivale"),
    ("Val Thorens in summer", "val-thorens-ete-diversification"),
    ("ALPÉON coordinates", "alpeon-gestion-200-proprietes"),
    ("Dynamic pricing", "tarification-dynamique-revpar"),
    ("Guaranteed rent vs. commission", "loyer-garanti-vs-commission"),
]

def fix_cards(path, base_url, CARDS):
    with open(path, encoding='utf-8') as f:
        html = f.read()

    for title_frag, slug in CARDS:
        # Find the article block containing this title fragment
        # Pattern: <article class="mag-card">...</article>
        # We need to replace <article class="mag-card"> with <a class="mag-card" href="...">
        # and </article> with </a>
        # But only for the specific card containing this title

        # Build a pattern that matches <article class="mag-card"> ... title_frag ... </article>
        # We'll do a simple string replacement around the title fragment

        # Find position of title fragment
        idx = html.find(title_frag)
        if idx == -1:
            print(f"WARNING: '{title_frag}' not found in {path}")
            continue

        # Find the <article class="mag-card"> before this fragment
        art_start = html.rfind('<article class="mag-card">', 0, idx)
        if art_start == -1:
            print(f"WARNING: No <article class='mag-card'> before '{title_frag}'")
            continue

        # Find the </article> after this fragment
        art_end = html.find('</article>', idx)
        if art_end == -1:
            print(f"WARNING: No </article> after '{title_frag}'")
            continue

        # Get the block
        original = html[art_start:art_end + len('</article>')]

        # Replace opening and closing tags
        replaced = original.replace(
            '<article class="mag-card">',
            f'<a class="mag-card" href="{base_url}{slug}/">',
            1
        ).replace('</article>', '</a>', 1)

        # Also remove the "Article à rédiger" badge from linked cards
        replaced = replaced.replace(
            '\n          <!-- TODO: Rédiger le contenu complet de cet article -->\n          <span class="mag-card-todo">Article à rédiger</span>',
            ''
        )
        replaced = replaced.replace(
            '\n          <!-- TODO: Rédiger le contenu complet de cet article -->\n          <span class="mag-card-todo">À rédiger</span>',
            ''
        )

        html = html[:art_start] + replaced + html[art_end + len('</article>'):]
        print(f"  ✓ Linked card: {title_frag} → {base_url}{slug}/")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Saved {path}")

# FR (already done, skip re-processing)
# fix_cards('/Users/edgarvernet/claude/alpeon/magazine/index.html', '/magazine/', CARDS_FR)
print()
# EN
fix_cards('/Users/edgarvernet/claude/alpeon/en/magazine/index.html', '/en/magazine/', CARDS_EN)
