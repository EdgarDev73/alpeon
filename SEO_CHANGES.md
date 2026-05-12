# SEO_CHANGES — branche `feat/seo-technical-fixes`

Récapitulatif des modifications techniques SEO effectuées sur ce projet.  
Branche : `feat/seo-technical-fixes` — à merger dans `main`.

---

## Ce qui a été fait

### Lot Pré-SEO — Fixes visuels & images (5 commits)

| Commit | Détail |
|---|---|
| `fix: light mode` | Estimateur pages : cartes `.how-step`, CTA, `.why-card` stylisés correctement en light mode |
| `fix: estimateur header` | Header `.site-header` match le fond sombre du héro (pas de fond blanc) |
| `fix: broken images (Ahrefs)` | 10 images 404 réparées : 6 photos équipe + 4 `.webp` destinations |
| `fix: replace Léa → Florine` | Équipe : remplacement complet (photo, nom, rôle, bio, initiale) FR+EN |
| `fix: Thomas Business Development` | Rôle Thomas mis à jour, bio reconstruite autour du développement portefeuille |

---

### COMMIT 1 — Fix destination links — home tiles + footer (P0 ★★★★★)

**Fichier** : `_scripts/fix_destination_links.py`

**Problème** : 6 tuiles destinations sur `accueil/` + tous les footers pointaient vers `/destinations/` (URL hub) au lieu des URLs dédiées des stations.

**Résultat** : 132 liens footer + 6 tuiles home corrigés (22 fichiers). Chaque ville pointe maintenant vers sa page dédiée.

Vérification :
```bash
grep -r 'href="/destinations/"' --include="*.html" | grep -v "Voir toutes\|À explorer\|destinations-all\|breadcrumb"
# → doit retourner 0
```

---

### COMMIT 2 — LinkedIn URL — ⏸ REPORTÉ

Le compte LinkedIn `linkedin.com/company/alpeon/` n'est pas encore créé.  
Marqueur `<!-- TODO: update to linkedin.com/company/alpeon/ once created -->` laissé dans les footers.  
Script à écrire et exécuter une fois le compte créé.

---

### COMMIT 3 — Maillage inter-stations complet (P0 ★★★★)

**Fichier** : `_scripts/fix_maillage_stations.py`

**Problème** : Chaque page station n'avait que 3 liens sur 5 vers les autres stations.

**Résultat** : 2 cartes manquantes ajoutées sur chacune des 6 pages FR. Pages EN meribel/tignes/val-d-isere vérifiées — déjà complètes (format compact différent).

| Station | Cartes ajoutées |
|---|---|
| Courchevel | Tignes, Val Thorens |
| Megève | Méribel, Tignes |
| Méribel | Megève, Tignes |
| Tignes | Megève, Méribel |
| Val d'Isère | Megève, Val Thorens |
| Val Thorens | Megève, Val d'Isère |

---

### COMMIT 4 — Organization JSON-LD enrichi (P0 ★★★)

**Fichier** : `_scripts/fix_organization_schema.py`

**Pages** : `accueil/index.html` + `en/accueil/index.html`

**Ajouts** :
- `"@type": ["RealEstateAgent", "LocalBusiness", "Organization"]` (ajout Organization)
- `alternateName: "Alpéon Alpine Property Management"`
- `logo: "https://alpeon.fr/assets/logo/logo-main-gold.svg"`
- `telephone: "+33970703991"`
- `parentOrganization: { "@type": "Organization", "name": "VerSpi Real Estate" }`
- `contactPoint` avec `availableLanguage: ["French", "English"]`
- `sameAs`: Instagram uniquement (LinkedIn en attente de compte)

---

### COMMIT 5 — Breadcrumb HTML sur pages internes (P0 ★★★)

**Fichiers** : `_scripts/add_breadcrumbs_internal.py` + `_scripts/add_breadcrumb_css.py`

**Problème** : `about`, `faq`, `contact`, `proprietaires` avaient BreadcrumbList JSON-LD mais pas de `<nav>` visible.

**Résultat** : `<nav class="breadcrumb" aria-label="Fil d'Ariane">` + CSS injectés sur 8 pages (FR+EN).

---

### COMMIT 6 — robots.txt : blocage routes API (P1 ★★)

**Fichier** : `robots.txt`

```
Disallow: /api/
Disallow: /email-estimation.html
Disallow: /resultats.html
```

---

### COMMIT 7 — Sitemap : lastmod mis à jour (P1 ★★)

**Fichier** : `sitemap.xml`

- Toutes les `<lastmod>` mises à `2026-05-08`
- Entrées loyer-garanti + magazine ajoutées dans les commits suivants

---

### COMMIT 8 — Page `/loyer-garanti/` + `/en/guaranteed-rent/` (P2 ★★★★)

**Fichiers créés** : `loyer-garanti/index.html`, `en/guaranteed-rent/index.html`

**Contenu FR** :
- Hero : "Un loyer fixe garanti chaque mois"
- Mécanique en 3 étapes
- Tableau comparatif : ALPÉON loyer garanti vs. gestion classique
- CTA estimateur
- FAQ 6 questions (→ FAQPage JSON-LD)
- CTA final

**JSON-LD** : BreadcrumbList + Service + FAQPage (6 questions FR / 4 EN)

**Navigation** :
- Footer "Services" : lien `/loyer-garanti/` ajouté dans 37 fichiers HTML
- `accueil/` + `en/accueil/` : card marque-résidences pointe vers loyer-garanti
- `proprietaires/` + `en/proprietaires/` : callout section "Loyer garanti — fixe chaque mois"
- Sitemap : entrées FR+EN ajoutées (priority 0.8)

---

### COMMIT 9 — Magazine scaffold (P2 ★★)

**Fichiers créés** : `magazine/index.html`, `en/magazine/index.html`

**Structure** : Hero, 4 catégories × 3 articles placeholder = 12 articles avec badges "Article à rédiger"

**Catégories** :
- Investir en station / Investing in resorts
- Fiscalité LMNP / LMNP Tax
- Stations / Resorts
- Vie d'opérateur / Operator insights

**JSON-LD** : BreadcrumbList + Blog

**Navigation** :
- Footer "Services" : lien `/magazine/` ajouté dans 38 fichiers HTML
- Sitemap : entrées FR+EN ajoutées (changefreq weekly, priority 0.7)

---

## Vérification post-merge

```bash
# 1. Zéro lien brisé vers /destinations/ (hors "Voir toutes")
grep -r 'href="/destinations/"' --include="*.html" | grep -v "Voir toutes\|À explorer"

# 2. Zéro LinkedIn jupiter-residences (toujours en attente)
grep -r 'jupiter-residences' --include="*.html"

# 3. Chaque page station a 5 liens vers les autres
for s in courchevel megeve meribel tignes val-d-isere val-thorens; do
  echo "$s: $(grep -c 'href="/destinations/' /destinations/$s/index.html)"
done

# 4. Breadcrumb visible sur pages internes
grep -l 'breadcrumb-list' about/index.html faq/index.html contact/index.html proprietaires/index.html

# 5. Valider le JSON-LD
# → https://search.google.com/test/rich-results sur : accueil/, destinations/courchevel/, loyer-garanti/

# 6. Search Console : soumettre sitemap.xml après merge
```

---

## TODO techniques restants

- [ ] **LinkedIn** : quand `linkedin.com/company/alpeon/` est créé, mettre à jour `sameAs` dans Organization schema (accueil FR+EN) et remplacer `jupiter-residences1` dans tous les footers. Script à écrire : `_scripts/fix_linkedin_url.py`
- [ ] **Magazine** : rédiger les 12 articles (4 catégories × 3). Stack recommandée : Sanity.io (headless CMS) + export HTML via webhook Vercel, ou fichiers Markdown + script Python de génération HTML
- [ ] **Article template** : créer un template HTML `magazine/article-template.html` une fois le premier article rédigé
- [ ] **Photos stations** : remplacer les images hero actuelles (`/assets/images/hero-accueil.jpg`) par des photos dédiées sur loyer-garanti et magazine
- [ ] **AggregateRating** : ajouter témoignages propriétaires pour le schema AggregateRating (besoin de 5+ avis)
- [ ] **Station content** : rédiger 300-500 mots de contenu éditorial sur chaque page station (6 pages FR + 6 EN)

---

## Actions non-techniques à coordonner

| Action | Responsable |
|---|---|
| Créer le compte LinkedIn `linkedin.com/company/alpeon/` | Marketing |
| Rédiger le contenu 300-500 mots par page station | Rédacteur SEO |
| Fournir les témoignages propriétaires (AggregateRating) | Commercial |
| Décider du CMS pour le magazine (Sanity vs. Markdown) | Tech/Marketing |
| Rédiger les 12 articles magazine placeholder | Rédacteur SEO |
| Photographier les propriétés pour hero loyer-garanti / magazine | Photo |
| Soumettre sitemap.xml dans Search Console après merge | SEO/Dev |
