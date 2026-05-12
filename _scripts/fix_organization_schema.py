#!/usr/bin/env python3
"""Enrich Organization JSON-LD on accueil pages (FR + EN)."""
import re, os

BASE = '/Users/edgarvernet/claude/alpeon'

FR_BLOCK = """{
        "@type": ["RealEstateAgent", "LocalBusiness", "Organization"],
        "@id": "https://alpeon.fr/#organization",
        "name": "ALPÉON",
        "alternateName": "Alpéon Alpine Property Management",
        "url": "https://alpeon.fr",
        "logo": "https://alpeon.fr/assets/logo/logo-main-gold.svg",
        "telephone": "+33970703991",
        "email": "proprietaires@alpeon.fr",
        "description": "Opérateur premium de gestion immobilière alpine. ALPÉON gère, opère et valorise les biens en location saisonnière dans les Alpes françaises.",
        "priceRange": "€€€€",
        "parentOrganization": { "@type": "Organization", "name": "VerSpi Real Estate" },
        "contactPoint": {
          "@type": "ContactPoint",
          "telephone": "+33970703991",
          "contactType": "customer service",
          "email": "contact@alpeon.fr",
          "availableLanguage": ["French", "English"]
        },
        "sameAs": ["https://www.instagram.com/alpeon.alps"],
        "areaServed": [
          {"@type":"Place","name":"Val Thorens"},
          {"@type":"Place","name":"Megève"},
          {"@type":"Place","name":"Courchevel"},
          {"@type":"Place","name":"Méribel"},
          {"@type":"Place","name":"Tignes"},
          {"@type":"Place","name":"Val d'Isère"}
        ]
      }"""

EN_BLOCK = """{
        "@type": ["RealEstateAgent", "LocalBusiness", "Organization"],
        "@id": "https://alpeon.fr/#organization",
        "name": "ALPÉON",
        "alternateName": "Alpéon Alpine Property Management",
        "url": "https://alpeon.fr",
        "logo": "https://alpeon.fr/assets/logo/logo-main-gold.svg",
        "telephone": "+33970703991",
        "email": "proprietaires@alpeon.fr",
        "description": "Premium alpine property management operator. ALPÉON manages, operates and enhances short-term rental properties across the French Alps.",
        "priceRange": "€€€€",
        "parentOrganization": { "@type": "Organization", "name": "VerSpi Real Estate" },
        "contactPoint": {
          "@type": "ContactPoint",
          "telephone": "+33970703991",
          "contactType": "customer service",
          "email": "contact@alpeon.fr",
          "availableLanguage": ["French", "English"]
        },
        "sameAs": ["https://www.instagram.com/alpeon.alps"],
        "areaServed": [
          {"@type":"Place","name":"Val Thorens"},
          {"@type":"Place","name":"Megève"},
          {"@type":"Place","name":"Courchevel"},
          {"@type":"Place","name":"Méribel"},
          {"@type":"Place","name":"Tignes"},
          {"@type":"Place","name":"Val d'Isère"}
        ]
      }"""

OLD_PATTERN = r'\{\s*"@type": \["RealEstateAgent", "LocalBusiness"\],\s*"@id": "https://alpeon\.fr/#organization".*?"areaServed": \[.*?\]\s*\}'

for fp, new_block in [(f'{BASE}/accueil/index.html', FR_BLOCK),
                       (f'{BASE}/en/accueil/index.html', EN_BLOCK)]:
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    new_content, n = re.subn(OLD_PATTERN, new_block, content, flags=re.DOTALL)
    if n:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'OK: {fp.replace(BASE, "")}')
    else:
        print(f'WARN: pattern not found in {fp.replace(BASE, "")}')
