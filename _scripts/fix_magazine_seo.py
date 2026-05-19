#!/usr/bin/env python3
"""
Fix SEO issues on all 12 magazine articles (Ahrefs audit 2026-05-19):
  1. <title> too long (> 60 chars) → shorten, remove ' | ALPÉON Magazine'
  2. <meta name="description"> too long (> 160 chars) → trim to ≤ 155 chars
  3. hreflang="en" pointing to 404 /en/magazine/* → remove those <link> tags
  4. Twitter card missing → add twitter:card/title/description/image
  5. Update sitemap.xml to include all 12 article URLs
"""
import os, re
from pathlib import Path
from datetime import date

BASE = Path(__file__).parent.parent

# ── 1.  Per-article overrides (title ≤ 60, desc ≤ 155) ──────────────────────
OVERRIDES = {
    "alpeon-gestion-200-proprietes": {
        "title": "Gérer 200 biens alpins : coulisses d'un opérateur premium",
        "desc":  "Comment ALPÉON organise la gestion de 200+ biens alpins. Organisation, technologie, standards housekeeping et relation propriétaires — transparence totale.",
    },
    "amortissement-lmnp-chalet": {
        "title": "Amortissement LMNP : optimiser la fiscalité de votre chalet",
        "desc":  "Comment fonctionne l'amortissement en LMNP réel pour un chalet alpin ? Mécanisme par composant, exemple chiffré complet et conseils d'optimisation.",
    },
    "investir-courchevel-2025": {
        "title": "Investir à Courchevel en 2025 : prix et rendements",
        "desc":  "Analyse du marché immobilier de Courchevel en 2025 : prix au m² par village, rendements locatifs attendus et conseils pour éviter les erreurs coûteuses.",
    },
    "lmnp-2025-guide-complet": {
        "title": "LMNP en 2025 : guide complet pour propriétaires alpins",
        "desc":  "Tout sur le LMNP en 2025 : conditions, régimes fiscaux, amortissement et stratégie pour les propriétaires de chalets et appartements alpins.",
    },
    "loyer-garanti-vs-commission": {
        "title": "Loyer garanti ou commission : quel modèle choisir ?",
        "desc":  "Comparatif loyer garanti vs gestion à la commission pour un bien de montagne. Avantages, risques et conditions d'éligibilité — tout pour choisir.",
    },
    "megeve-demande-estivale": {
        "title": "Megève en été : montée en puissance d'un marché premium",
        "desc":  "Comment la demande estivale transforme Megève en destination 4 saisons premium. Tendances, prix de location et conseils pour maximiser vos revenus.",
    },
    "micro-bic-vs-regime-reel": {
        "title": "Micro-BIC vs. régime réel LMNP : quel choix ?",
        "desc":  "Micro-BIC ou régime réel en LMNP : comparatif chiffré pour un appartement alpin, avantages et limites de chaque option et guide pour basculer.",
    },
    "neuf-vs-ancien-station-ski": {
        "title": "Neuf ou ancien en station de ski : que disent les chiffres ?",
        "desc":  "Neuf ou ancien en station alpine : avantages fiscaux du neuf, liberté de l'ancien, comparatif sur 10 ans. Ce guide vous aide à faire le bon choix.",
    },
    "tarification-dynamique-revpar": {
        "title": "Tarification dynamique et RevPAR : maximiser vos revenus",
        "desc":  "Comment la tarification dynamique et le RevPAR permettent d'optimiser les revenus locatifs d'un bien alpin. Méthode, outils et exemples ALPÉON.",
    },
    "tignes-saison-2024-2025": {
        "title": "Tignes 2024/2025 : bilan d'une saison record",
        "desc":  "Bilan de la saison hivernale 2024/2025 à Tignes : enneigement, taux d'occupation, prix de nuitée et perspectives pour les propriétaires Espace Killy.",
    },
    "val-d-isere-vs-meribel-rendement-locatif": {
        "title": "Val d'Isère vs. Méribel : quel rendement locatif ?",
        "desc":  "Comparatif entre Val d'Isère et Méribel : prix au m², profil de clientèle, durée de saison et rendements. Quel marché selon votre profil d'investisseur ?",
    },
    "val-thorens-ete-diversification": {
        "title": "Val Thorens : du ski exclusif à la destination 4 saisons",
        "desc":  "Comment Val Thorens, la station la plus haute d'Europe, se réinvente en été. Projets, vélo, événements et impact sur les rendements locatifs.",
    },
}

# Validate lengths
errors = []
for slug, ov in OVERRIDES.items():
    if len(ov["title"]) > 60:
        errors.append(f"TITLE too long ({len(ov['title'])}): {slug}")
    if len(ov["desc"]) > 155:
        errors.append(f"DESC too long ({len(ov['desc'])}): {slug}")
if errors:
    for e in errors: print("ERROR:", e)
    raise SystemExit(1)

changed = 0

for slug, ov in OVERRIDES.items():
    path = BASE / "magazine" / slug / "index.html"
    if not path.exists():
        print(f"SKIP (not found): {slug}")
        continue

    html = path.read_text(encoding="utf-8")
    original = html

    # ── Fix <title> ──────────────────────────────────────────────────────────
    html = re.sub(
        r'<title>[^<]+</title>',
        f'<title>{ov["title"]}</title>',
        html
    )

    # ── Fix <meta name="description"> ───────────────────────────────────────
    html = re.sub(
        r'(<meta\s+name="description"\s+content=")[^"]*(")',
        lambda m: m.group(1) + ov["desc"] + m.group(2),
        html
    )

    # ── Remove hreflang="en" pointing to /en/magazine/* ─────────────────────
    html = re.sub(
        r'\s*<link rel="alternate" hreflang="en" href="https://alpeon\.fr/en/magazine/[^"]*" />\n?',
        '\n',
        html
    )

    # ── Add Twitter card tags (after og:image, only if not already present) ─
    if 'twitter:card' not in html:
        twitter_block = (
            f'\n  <meta name="twitter:card" content="summary_large_image" />\n'
            f'  <meta name="twitter:title" content="{ov["title"]}" />\n'
            f'  <meta name="twitter:description" content="{ov["desc"]}" />\n'
            f'  <meta name="twitter:image" content="https://alpeon.fr/assets/images/hero-accueil.jpg" />'
        )
        html = html.replace(
            '<meta property="og:image" content="https://alpeon.fr/assets/images/hero-accueil.jpg" />',
            '<meta property="og:image" content="https://alpeon.fr/assets/images/hero-accueil.jpg" />'
            + twitter_block
        )

    if html != original:
        path.write_text(html, encoding="utf-8")
        print(f"  ✓ fixed: {slug}")
        changed += 1
    else:
        print(f"  ~ no change: {slug}")

print(f"\nArticles fixed: {changed}/12")

# ── 2. Update sitemap.xml ────────────────────────────────────────────────────
sitemap_path = BASE / "sitemap.xml"
sitemap = sitemap_path.read_text(encoding="utf-8")
today = date.today().isoformat()

# Build the 12 new <url> entries (FR only — no EN versions exist yet)
ARTICLE_ENTRIES = ""
for slug in OVERRIDES:
    url = f"https://alpeon.fr/magazine/{slug}/"
    entry = f"""
  <url>
    <loc>{url}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
    <xhtml:link rel="alternate" hreflang="fr"        href="{url}"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="{url}"/>
  </url>"""
    # Only add if not already present
    if slug not in sitemap:
        ARTICLE_ENTRIES += entry

if ARTICLE_ENTRIES:
    # Insert before </urlset>
    sitemap = sitemap.replace("</urlset>", ARTICLE_ENTRIES + "\n</urlset>")
    sitemap_path.write_text(sitemap, encoding="utf-8")
    print(f"\n✓ sitemap.xml updated (+{ARTICLE_ENTRIES.count('<url>')} articles)")
else:
    print("\n~ sitemap.xml already up to date")

print("\nDone.")
