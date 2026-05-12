#!/usr/bin/env python3
"""
Create /loyer-garanti/ (FR) and /en/guaranteed-rent/ (EN) pages.
Extracts nav/footer from proprietaires, inserts new content.
"""
import os

BASE = '/Users/edgarvernet/claude/alpeon'

with open(f'{BASE}/proprietaires/index.html', 'r', encoding='utf-8') as f:
    prop_lines = f.readlines()
prop = ''.join(prop_lines)

# Extract nav block (lines 75-764 roughly — the @@NAV-START@@ to closing </style>)
nav_start = prop.find('/* @@NAV-START@@ */')
nav_end = prop.find('/* @@NAV-END@@ */') + len('/* @@NAV-END@@ */')
nav_css = prop[nav_start:nav_end]

# Extract header HTML (the <header> element)
header_start = prop.find('<header class="site-header"')
header_end = prop.find('</header>') + len('</header>')
header_html = prop[header_start:header_end]

# Extract footer HTML
footer_start = prop.find('<!-- FOOTER -->')
footer_end = len(prop)
footer_html = prop[footer_start:]

# ── FR PAGE ──
FR_HTML = f'''<!DOCTYPE html>
<html lang="fr">
<head>
  <!-- Consent Mode v2 — RGPD (avant GTM) -->
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    var _ac = localStorage.getItem('alpeon_cookie_consent');
    gtag('consent', 'default', {{
      'analytics_storage': _ac === 'granted' ? 'granted' : 'denied',
      'ad_storage': 'denied',
      'wait_for_update': 500
    }});
  </script>
  <!-- Google Tag Manager -->
  <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','GTM-PXZ2KXWV');</script>
  <!-- End Google Tag Manager -->
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-XCYNTWQ9HX"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-XCYNTWQ9HX');
  </script>
  <meta charset="UTF-8" />
  <link rel="icon" type="image/x-icon" href="/assets/logo/favicon.ico">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/logo/favicon-32.png">
  <link rel="icon" type="image/png" sizes="180x180" href="/assets/logo/favicon-180.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/logo/favicon-180.png">
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Loyer Garanti Propriétaire — Revenus Alpins Garantis | ALPÉON</title>
  <meta name="description" content="ALPÉON garantit votre loyer chaque mois, que votre bien soit occupé ou non. Découvrez comment fonctionne le loyer garanti pour les propriétaires de biens alpins." />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="https://alpeon.fr/loyer-garanti/" />
  <link rel="alternate" hreflang="fr" href="https://alpeon.fr/loyer-garanti/" />
  <link rel="alternate" hreflang="en" href="https://alpeon.fr/en/guaranteed-rent/" />
  <link rel="alternate" hreflang="x-default" href="https://alpeon.fr/loyer-garanti/" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="Loyer Garanti Propriétaire — Revenus Alpins Garantis | ALPÉON" />
  <meta property="og:description" content="Percevez un loyer fixe chaque mois, quelle que soit l'occupation de votre chalet ou appartement alpin. La formule ALPÉON loyer garanti." />
  <meta property="og:url" content="https://alpeon.fr/loyer-garanti/" />
  <meta property="og:image" content="https://alpeon.fr/assets/images/hero-accueil.jpg" />
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "BreadcrumbList",
        "itemListElement": [
          {{ "@type": "ListItem", "position": 1, "name": "Accueil", "item": "https://alpeon.fr/accueil/" }},
          {{ "@type": "ListItem", "position": 2, "name": "Loyer garanti", "item": "https://alpeon.fr/loyer-garanti/" }}
        ]
      }},
      {{
        "@type": "Service",
        "name": "Loyer garanti — ALPÉON",
        "provider": {{ "@type": "Organization", "@id": "https://alpeon.fr/#organization" }},
        "serviceType": "Gestion locative avec revenu garanti",
        "description": "ALPÉON verse un loyer fixe mensuel au propriétaire, indépendamment du taux d'occupation. Couvre Courchevel, Megève, Méribel, Tignes, Val d'Isère et Val Thorens.",
        "areaServed": ["Courchevel", "Megève", "Méribel", "Tignes", "Val d'Isère", "Val Thorens"]
      }},
      {{
        "@type": "FAQPage",
        "mainEntity": [
          {{
            "@type": "Question",
            "name": "Qu'est-ce que le loyer garanti ALPÉON ?",
            "acceptedAnswer": {{ "@type": "Answer", "text": "Le loyer garanti ALPÉON est une formule dans laquelle ALPÉON devient votre locataire direct. Nous vous versons un loyer fixe chaque mois, que votre bien soit loué ou vide. Zéro aléa, zéro vacance locative." }}
          }},
          {{
            "@type": "Question",
            "name": "Comment est calculé le montant du loyer garanti ?",
            "acceptedAnswer": {{ "@type": "Answer", "text": "Le loyer garanti est calculé selon la surface du bien, sa localisation (station et altitude), son standing et la saisonnalité locale. Notre estimateur en ligne fournit une fourchette personnalisée en moins de 2 minutes." }}
          }},
          {{
            "@type": "Question",
            "name": "Puis-je utiliser mon bien personnellement avec un loyer garanti ?",
            "acceptedAnswer": {{ "@type": "Answer", "text": "Oui. Lors de la signature du contrat, des périodes de blocage personnel peuvent être prévues. Le loyer garanti est alors calculé en tenant compte de ces périodes d'exclusivité." }}
          }},
          {{
            "@type": "Question",
            "name": "Quelle est la durée minimale du contrat loyer garanti ?",
            "acceptedAnswer": {{ "@type": "Answer", "text": "Les contrats ALPÉON loyer garanti sont généralement conclus pour 1 à 3 saisons, renouvelables. Un préavis de 3 mois avant la saison est requis pour mettre fin au contrat." }}
          }},
          {{
            "@type": "Question",
            "name": "Le loyer garanti couvre-t-il les dommages au bien ?",
            "acceptedAnswer": {{ "@type": "Answer", "text": "ALPÉON prend en charge l'entretien courant et la remise en état après chaque séjour. Pour les dommages exceptionnels, une assurance propriétaire non occupant (PNO) complémentaire est recommandée." }}
          }},
          {{
            "@type": "Question",
            "name": "Dans quelles stations alpines le loyer garanti est-il disponible ?",
            "acceptedAnswer": {{ "@type": "Answer", "text": "La formule loyer garanti ALPÉON est disponible à Courchevel, Megève, Méribel, Tignes, Val d'Isère et Val Thorens — les 6 stations alpines où nous opérons plus de 200 propriétés." }}
          }}
        ]
      }}
    ]
  }}
  </script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Yeseva+One&display=swap" rel="stylesheet" />
  <link href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400;1,500;1,600&display=swap" rel="stylesheet" />

  <style>
  :root {{
    --green: #2C3D30; --green-d: #223028; --gold: #E8CBA0; --gold-d: #D4B48A;
    --ink: #0d1a0f; --white: #FAFEFF; --stone-1: #F5F3EF; --stone-2: #EAE6DF;
    --black: #111111; --mid: #4A5C4E;
    --font-sans: 'Poppins', sans-serif; --font-serif: 'Yeseva One', serif;
    --nav-h: 88px; --max: 1380px; --pad: clamp(24px, 5vw, 80px);
  }}
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html {{ scroll-behavior: smooth; -webkit-font-smoothing: antialiased; }}
  body {{ font-family: var(--font-sans); font-weight: 300; background: var(--ink); color: rgba(250,254,255,.85); line-height: 1.6; overflow-x: hidden; }}
  img {{ display: block; max-width: 100%; }}
  a {{ text-decoration: none; color: inherit; }}
  ul {{ list-style: none; }}
  .container {{ width: 100%; max-width: var(--max); margin: 0 auto; padding: 0 var(--pad); }}

  {nav_css}

  /* ── PAGE STYLES ── */
  .lg-hero {{ padding: calc(var(--nav-h) + 80px) var(--pad) 90px; text-align: center; max-width: 820px; margin: 0 auto; }}
  .lg-eyebrow {{ font-size: .72rem; letter-spacing: .2em; text-transform: uppercase; color: var(--gold); opacity: .8; margin-bottom: 1.5rem; }}
  .lg-hero h1 {{ font-family: var(--font-serif); font-size: clamp(2.2rem, 5vw, 3.8rem); font-weight: 400; line-height: 1.15; margin-bottom: 1.5rem; color: #fff; }}
  .lg-hero h1 em {{ font-style: italic; color: var(--gold); }}
  .lg-hero-sub {{ font-size: 1.05rem; color: rgba(250,254,255,.55); max-width: 560px; margin: 0 auto 2.5rem; line-height: 1.8; }}
  .lg-hero-cta {{ display: inline-flex; align-items: center; gap: .6rem; background: var(--gold); color: var(--ink); padding: .9rem 2rem; border-radius: 4px; font-size: .8rem; font-weight: 600; letter-spacing: .12em; text-transform: uppercase; transition: background .2s; }}
  .lg-hero-cta:hover {{ background: var(--gold-d); }}

  /* Steps */
  .lg-steps {{ background: rgba(44,61,48,.18); border-top: 1px solid rgba(232,203,160,.06); border-bottom: 1px solid rgba(232,203,160,.06); padding: 80px var(--pad); }}
  .lg-steps-inner {{ max-width: var(--max); margin: 0 auto; }}
  .lg-steps-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 2.5rem; margin-top: 3.5rem; }}
  @media (max-width: 760px) {{ .lg-steps-grid {{ grid-template-columns: 1fr; max-width: 480px; margin-inline: auto; }} }}
  .lg-step {{ padding: 2rem; background: rgba(255,255,255,.04); border: 1px solid rgba(232,203,160,.12); border-radius: 12px; }}
  .lg-step-num {{ width: 44px; height: 44px; border: 1px solid rgba(232,203,160,.3); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-family: var(--font-serif); font-size: 1rem; color: var(--gold); margin-bottom: 1.25rem; }}
  .lg-step h3 {{ font-size: .95rem; font-weight: 500; color: rgba(250,254,255,.9); margin-bottom: .6rem; }}
  .lg-step p {{ font-size: .83rem; color: rgba(250,254,255,.45); line-height: 1.75; }}

  /* Comparatif */
  .lg-compare {{ padding: 80px var(--pad); max-width: var(--max); margin: 0 auto; }}
  .lg-compare-table {{ width: 100%; border-collapse: collapse; margin-top: 2.5rem; }}
  .lg-compare-table th, .lg-compare-table td {{ padding: 1rem 1.25rem; text-align: left; border-bottom: 1px solid rgba(232,203,160,.08); font-size: .85rem; }}
  .lg-compare-table thead th {{ font-size: .72rem; letter-spacing: .12em; text-transform: uppercase; color: rgba(250,254,255,.4); font-weight: 400; }}
  .lg-compare-table thead th:nth-child(2) {{ color: var(--gold); }}
  .lg-compare-table td:nth-child(2) {{ color: rgba(250,254,255,.9); }}
  .lg-compare-table td:nth-child(1) {{ color: rgba(250,254,255,.6); }}
  .lg-compare-table td:nth-child(3) {{ color: rgba(250,254,255,.35); }}
  .check {{ color: #7ecb8f; }}
  .cross {{ color: rgba(250,100,100,.6); }}
  @media (max-width: 640px) {{ .lg-compare-table th, .lg-compare-table td {{ padding: .7rem .6rem; font-size: .78rem; }} }}

  /* Estimateur CTA */
  .lg-est {{ padding: 80px var(--pad); background: rgba(44,61,48,.25); border-top: 1px solid rgba(232,203,160,.06); text-align: center; }}
  .lg-est-inner {{ max-width: 620px; margin: 0 auto; }}
  .lg-est h2 {{ font-family: var(--font-serif); font-size: clamp(1.6rem, 3.5vw, 2.4rem); color: #fff; margin-bottom: 1rem; }}
  .lg-est h2 em {{ font-style: italic; color: var(--gold); }}
  .lg-est p {{ color: rgba(250,254,255,.5); margin-bottom: 2rem; font-size: .9rem; }}

  /* FAQ */
  .lg-faq {{ padding: 80px var(--pad); max-width: 760px; margin: 0 auto; }}
  .lg-faq h2 {{ font-family: var(--font-serif); font-size: clamp(1.6rem, 3.5vw, 2.2rem); color: #fff; margin-bottom: 2.5rem; }}
  .faq-item {{ border-bottom: 1px solid rgba(232,203,160,.1); }}
  .faq-q {{ width: 100%; background: none; border: none; text-align: left; padding: 1.25rem 0; cursor: pointer; display: flex; justify-content: space-between; align-items: center; gap: 1rem; color: rgba(250,254,255,.9); font-size: .92rem; font-family: var(--font-sans); font-weight: 400; line-height: 1.5; }}
  .faq-q:hover {{ color: #fff; }}
  .faq-icon {{ width: 28px; height: 28px; border: 1px solid rgba(232,203,160,.2); border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }}
  .faq-icon svg {{ width: 12px; height: 12px; stroke: rgba(250,254,255,.6); transition: transform .25s; }}
  .faq-item.open .faq-icon svg {{ transform: rotate(45deg); }}
  .faq-a {{ display: none; padding: 0 0 1.25rem; color: rgba(250,254,255,.45); font-size: .85rem; line-height: 1.75; }}
  .faq-item.open .faq-a {{ display: block; }}

  /* CTA final */
  .lg-cta {{ padding: 90px var(--pad); background: var(--green); text-align: center; }}
  .lg-cta-inner {{ max-width: 640px; margin: 0 auto; }}
  .lg-cta-eyebrow {{ font-size: .72rem; letter-spacing: .2em; text-transform: uppercase; color: rgba(232,203,160,.7); margin-bottom: 1.25rem; }}
  .lg-cta h2 {{ font-family: var(--font-serif); font-size: clamp(1.8rem, 4vw, 2.8rem); color: #fff; margin-bottom: 1rem; }}
  .lg-cta h2 em {{ font-style: italic; color: var(--gold); }}
  .lg-cta p {{ color: rgba(250,254,255,.6); margin-bottom: 2.5rem; font-size: .95rem; }}
  .lg-cta-btns {{ display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; }}
  .btn-primary {{ display: inline-flex; align-items: center; gap: .5rem; background: var(--gold); color: var(--ink); padding: .9rem 2rem; border-radius: 4px; font-size: .8rem; font-weight: 600; letter-spacing: .1em; text-transform: uppercase; transition: background .2s; }}
  .btn-primary:hover {{ background: var(--gold-d); }}
  .btn-ghost {{ display: inline-flex; align-items: center; gap: .5rem; border: 1px solid rgba(232,203,160,.4); color: rgba(250,254,255,.7); padding: .9rem 2rem; border-radius: 4px; font-size: .8rem; font-weight: 500; letter-spacing: .1em; text-transform: uppercase; transition: all .2s; }}
  .btn-ghost:hover {{ border-color: var(--gold); color: var(--gold); }}

  /* Sec titles shared */
  .sec-eyebrow {{ font-size: .72rem; letter-spacing: .2em; text-transform: uppercase; color: var(--gold); opacity: .8; margin-bottom: 1rem; }}
  .sec-title {{ font-family: var(--font-serif); font-size: clamp(1.8rem, 4vw, 2.6rem); font-weight: 400; line-height: 1.2; color: #fff; }}
  .sec-title em {{ font-style: italic; color: var(--gold); }}
  .sec-desc {{ color: rgba(250,254,255,.45); margin-top: .75rem; font-size: .9rem; max-width: 540px; line-height: 1.8; }}

  /* Breadcrumb */
  .breadcrumb {{ padding: .75rem 0; }}
  .breadcrumb-list {{ display: flex; align-items: center; gap: .4rem; list-style: none; flex-wrap: wrap; }}
  .breadcrumb-list li {{ display: flex; align-items: center; gap: .4rem; }}
  .breadcrumb-list li::before {{ content: '›'; color: rgba(250,254,255,.25); font-size: .8rem; }}
  .breadcrumb-list li:first-child::before {{ display: none; }}
  .breadcrumb-list a {{ color: rgba(250,254,255,.35); font-size: .72rem; letter-spacing: .06em; text-transform: uppercase; transition: color .2s; }}
  .breadcrumb-list a:hover {{ color: var(--gold); }}
  .breadcrumb-list span {{ color: rgba(250,254,255,.55); font-size: .72rem; letter-spacing: .06em; text-transform: uppercase; }}
  </style>
</head>
<body>
  <!-- Google Tag Manager (noscript) -->
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-PXZ2KXWV" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>

  {header_html}

  <!-- BREADCRUMB -->
  <div class="container" style="padding-top: calc(var(--nav-h) + 1rem)">
    <nav class="breadcrumb" aria-label="Fil d'Ariane">
      <ol class="breadcrumb-list">
        <li><a href="/accueil/">Accueil</a></li>
        <li><span>Loyer garanti</span></li>
      </ol>
    </nav>
  </div>

  <!-- HERO -->
  <section style="padding-top:0">
    <div class="lg-hero">
      <div class="lg-eyebrow">Formule exclusive ALPÉON</div>
      <h1>Un loyer fixe <em>garanti</em><br>chaque mois</h1>
      <p class="lg-hero-sub">Que votre chalet soit loué 20 nuits ou 80, vous percevez le même montant. ALPÉON devient votre locataire direct — zéro vacance, zéro aléa.</p>
      <a href="/estimateur/" class="lg-hero-cta">
        Calculer mon loyer garanti
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
      </a>
    </div>
  </section>

  <!-- STEPS -->
  <section class="lg-steps">
    <div class="lg-steps-inner">
      <div class="sec-eyebrow" style="text-align:center">Comment ça marche</div>
      <h2 class="sec-title" style="text-align:center;margin-bottom:0">La mécanique en <em>3 étapes</em></h2>
      <div class="lg-steps-grid">
        <div class="lg-step">
          <div class="lg-step-num">01</div>
          <h3>Estimation personnalisée</h3>
          <p>Notre estimateur calcule la fourchette de loyer garanti pour votre bien en 2 minutes — surface, standing, station, localisation.</p>
        </div>
        <div class="lg-step">
          <div class="lg-step-num">02</div>
          <h3>Signature du mandat</h3>
          <p>ALPÉON devient votre locataire direct. Nous fixons contractuellement le montant mensuel et les conditions pour toute la durée du contrat.</p>
        </div>
        <div class="lg-step">
          <div class="lg-step-num">03</div>
          <h3>Virement mensuel garanti</h3>
          <p>Chaque mois, à date fixe, votre loyer est versé — qu'il y ait 0 ou 10 séjours ce mois-là. Vous suivez tout depuis votre espace propriétaire.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- COMPARATIF -->
  <section style="background:rgba(44,61,48,.08); border-top:1px solid rgba(232,203,160,.06)">
    <div class="lg-compare">
      <div class="sec-eyebrow">Pourquoi choisir ALPÉON</div>
      <h2 class="sec-title">Loyer garanti <em>vs.</em> gestion classique</h2>
      <p class="sec-desc">La différence fondamentale : avec ALPÉON, votre revenu ne dépend plus des voyageurs.</p>
      <table class="lg-compare-table">
        <thead>
          <tr>
            <th>Critère</th>
            <th>ALPÉON loyer garanti</th>
            <th>Gestion classique</th>
          </tr>
        </thead>
        <tbody>
          <tr><td>Revenu mensuel</td><td><span class="check">✓</span> Fixe et contractuel</td><td><span class="cross">✗</span> Variable selon l'occupation</td></tr>
          <tr><td>Vacances locatives</td><td><span class="check">✓</span> Aucun impact sur vos revenus</td><td><span class="cross">✗</span> Semaines vides = zéro revenu</td></tr>
          <tr><td>Gestion opérationnelle</td><td><span class="check">✓</span> Entièrement prise en charge</td><td><span class="cross">✗</span> Coordination partielle</td></tr>
          <tr><td>Transparence</td><td><span class="check">✓</span> Tableau de bord propriétaire</td><td><span class="cross">✗</span> Reporting souvent mensuel</td></tr>
          <tr><td>Périodes personnelles</td><td><span class="check">✓</span> Planifiables à la signature</td><td>Selon disponibilité</td></tr>
          <tr><td>Entretien courant</td><td><span class="check">✓</span> Inclus dans le contrat</td><td>Selon formule</td></tr>
        </tbody>
      </table>
    </div>
  </section>

  <!-- ESTIMATEUR CTA -->
  <section class="lg-est">
    <div class="lg-est-inner">
      <div class="sec-eyebrow">Estimateur gratuit</div>
      <h2>Combien rapporte votre bien <em>avec ALPÉON</em> ?</h2>
      <p>Obtenez une fourchette personnalisée en moins de 2 minutes. Gratuit, sans engagement.</p>
      <a href="/estimateur/" class="lg-hero-cta">
        Lancer l'estimation
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
      </a>
    </div>
  </section>

  <!-- FAQ -->
  <section style="background:rgba(44,61,48,.12)">
    <div class="lg-faq">
      <h2>Questions fréquentes sur le <em style="font-style:italic;color:var(--gold)">loyer garanti</em></h2>
      <div class="faq-item">
        <button class="faq-q" onclick="this.parentElement.classList.toggle('open')">
          Qu'est-ce que le loyer garanti ALPÉON ?
          <span class="faq-icon"><svg viewBox="0 0 24 24" fill="none" stroke-width="2.5"><path d="M12 5v14M5 12h14"/></svg></span>
        </button>
        <p class="faq-a">Le loyer garanti ALPÉON est une formule dans laquelle ALPÉON devient votre locataire direct. Nous vous versons un loyer fixe chaque mois, que votre bien soit loué ou vide. Zéro aléa, zéro vacance locative.</p>
      </div>
      <div class="faq-item">
        <button class="faq-q" onclick="this.parentElement.classList.toggle('open')">
          Comment est calculé le montant du loyer garanti ?
          <span class="faq-icon"><svg viewBox="0 0 24 24" fill="none" stroke-width="2.5"><path d="M12 5v14M5 12h14"/></svg></span>
        </button>
        <p class="faq-a">Le loyer garanti est calculé selon la surface du bien, sa localisation (station et altitude), son standing et la saisonnalité locale. Notre estimateur en ligne fournit une fourchette personnalisée en moins de 2 minutes.</p>
      </div>
      <div class="faq-item">
        <button class="faq-q" onclick="this.parentElement.classList.toggle('open')">
          Puis-je utiliser mon bien personnellement ?
          <span class="faq-icon"><svg viewBox="0 0 24 24" fill="none" stroke-width="2.5"><path d="M12 5v14M5 12h14"/></svg></span>
        </button>
        <p class="faq-a">Oui. Des périodes de blocage personnel peuvent être prévues à la signature du contrat. Le loyer garanti est calculé en tenant compte de ces périodes d'exclusivité.</p>
      </div>
      <div class="faq-item">
        <button class="faq-q" onclick="this.parentElement.classList.toggle('open')">
          Quelle est la durée minimale du contrat ?
          <span class="faq-icon"><svg viewBox="0 0 24 24" fill="none" stroke-width="2.5"><path d="M12 5v14M5 12h14"/></svg></span>
        </button>
        <p class="faq-a">Les contrats ALPÉON loyer garanti sont généralement conclus pour 1 à 3 saisons, renouvelables. Un préavis de 3 mois avant la saison est requis pour mettre fin au contrat.</p>
      </div>
      <div class="faq-item">
        <button class="faq-q" onclick="this.parentElement.classList.toggle('open')">
          Le loyer garanti couvre-t-il les dommages au bien ?
          <span class="faq-icon"><svg viewBox="0 0 24 24" fill="none" stroke-width="2.5"><path d="M12 5v14M5 12h14"/></svg></span>
        </button>
        <p class="faq-a">ALPÉON prend en charge l'entretien courant et la remise en état après chaque séjour. Pour les dommages exceptionnels, une assurance propriétaire non occupant (PNO) complémentaire est recommandée.</p>
      </div>
      <div class="faq-item">
        <button class="faq-q" onclick="this.parentElement.classList.toggle('open')">
          Dans quelles stations le loyer garanti est-il disponible ?
          <span class="faq-icon"><svg viewBox="0 0 24 24" fill="none" stroke-width="2.5"><path d="M12 5v14M5 12h14"/></svg></span>
        </button>
        <p class="faq-a">Disponible à Courchevel, Megève, Méribel, Tignes, Val d'Isère et Val Thorens — les 6 stations alpines où ALPÉON opère plus de 200 propriétés.</p>
      </div>
    </div>
  </section>

  <!-- CTA FINAL -->
  <section class="lg-cta">
    <div class="lg-cta-inner">
      <div class="lg-cta-eyebrow">Propriétaire d'un bien alpin</div>
      <h2>Votre bien mérite un <em>revenu garanti</em></h2>
      <p>Rejoignez les propriétaires ALPÉON qui perçoivent un loyer fixe chaque mois, en toute tranquillité.</p>
      <div class="lg-cta-btns">
        <a href="/estimateur/" class="btn-primary">Estimer mon loyer garanti</a>
        <a href="/contact/" class="btn-ghost">Parler à un expert</a>
      </div>
    </div>
  </section>

  {footer_html}

<script>
(function(){{
  var h=document.getElementById('site-header');
  if(!h)return;
  function u(){{h.classList.toggle('scrolled',window.scrollY>40);}}
  window.addEventListener('scroll',u,{{passive:true}});
  u();
}})();
(function(){{
  var wrap=document.getElementById('hdr-lang-wrap');
  var drop=document.getElementById('hdr-lang-dropdown');
  if(!wrap||!drop)return;
  var links=document.querySelectorAll('.site-lang a');
  links.forEach(function(a){{
    var item=document.createElement('a');
    item.href=a.href;
    item.className='hdr-lang-item'+(a.classList.contains('active')?' active':'');
    item.textContent=a.textContent.trim();
    drop.appendChild(item);
  }});
  document.addEventListener('click',function(e){{if(!wrap.contains(e.target))wrap.classList.remove('open');}});
}})();
function toggleLangDropdown(){{
  var wrap=document.getElementById('hdr-lang-wrap');
  if(!wrap)return;
  wrap.classList.toggle('open');
}}
async function submitNewsletter(e){{
  e.preventDefault();
  const email=document.getElementById('nl-email').value;
  document.getElementById('nl-msg').textContent='Merci ! Vous êtes inscrit.';
}}
</script>
</body>
</html>'''

# Create directories and write files
os.makedirs(f'{BASE}/loyer-garanti', exist_ok=True)
with open(f'{BASE}/loyer-garanti/index.html', 'w', encoding='utf-8') as f:
    f.write(FR_HTML)
print('Created: loyer-garanti/index.html')

# ── EN PAGE — simplified version ──
EN_FOOTER = footer_html.replace(
    "Propriétaire d'un bien alpin ?", "Do you own an alpine property?"
).replace(
    "Estimez vos revenus", "Estimate your rental income"
).replace(
    '/estimateur/', '/en/estimateur/'
).replace(
    '/proprietaires/', '/en/proprietaires/'
).replace(
    '/about/', '/en/about/'
).replace(
    '/faq/', '/en/faq/'
).replace(
    '/contact/', '/en/contact/'
).replace(
    '/destinations/courchevel/', '/en/destinations/courchevel/'
).replace(
    '/destinations/megeve/', '/en/destinations/megeve/'
).replace(
    '/destinations/val-d-isere/', '/en/destinations/val-d-isere/'
).replace(
    '/destinations/val-thorens/', '/en/destinations/val-thorens/'
).replace(
    '/destinations/meribel/', '/en/destinations/meribel/'
).replace(
    '/destinations/tignes/', '/en/destinations/tignes/'
).replace(
    '/mentions-legales/', '/en/mentions-legales/'
).replace(
    '/politique-confidentialite/', '/en/politique-confidentialite/'
).replace(
    '/cgv/', '/en/cgv/'
).replace(
    "Opérateur premium de gestion locative courte durée dans les Alpes françaises. Discrétion, excellence et transparence.",
    "Premium short-term rental operator in the French Alps. Discretion, excellence and transparency."
).replace(
    "Nouvelles propriétés, offres de saison et actualités alpines.",
    "New properties, seasonal offers and alpine news."
).replace(
    "votre@email.fr", "your@email.com"
).replace(
    "S'inscrire", "Subscribe"
).replace(
    "© 2026 ALPÉON. Tous droits réservés.", "© 2026 ALPÉON. All rights reserved."
).replace(
    "ALPÉON est une marque de VerSpi Real Estate", "ALPÉON is a brand of VerSpi Real Estate"
).replace(
    "Gestion locative alpine premium · Alpes françaises", "Premium Alpine Property Management · French Alps"
).replace(
    "Besoin d'aide ?", "Need help?"
)

EN_HTML = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Consent Mode v2 -->
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    var _ac = localStorage.getItem('alpeon_cookie_consent');
    gtag('consent', 'default', {{
      'analytics_storage': _ac === 'granted' ? 'granted' : 'denied',
      'ad_storage': 'denied',
      'wait_for_update': 500
    }});
  </script>
  <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','GTM-PXZ2KXWV');</script>
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-XCYNTWQ9HX"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-XCYNTWQ9HX');
  </script>
  <meta charset="UTF-8" />
  <link rel="icon" type="image/x-icon" href="/assets/logo/favicon.ico">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/logo/favicon-32.png">
  <link rel="icon" type="image/png" sizes="180x180" href="/assets/logo/favicon-180.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/logo/favicon-180.png">
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Guaranteed Rent — Alpine Property Income Guaranteed | ALPÉON</title>
  <meta name="description" content="ALPÉON guarantees your rental income every month, whether your alpine property is occupied or not. Fixed monthly payment, no vacancy risk." />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="https://alpeon.fr/en/guaranteed-rent/" />
  <link rel="alternate" hreflang="en" href="https://alpeon.fr/en/guaranteed-rent/" />
  <link rel="alternate" hreflang="fr" href="https://alpeon.fr/loyer-garanti/" />
  <link rel="alternate" hreflang="x-default" href="https://alpeon.fr/loyer-garanti/" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="Guaranteed Rent — Alpine Property Income Guaranteed | ALPÉON" />
  <meta property="og:url" content="https://alpeon.fr/en/guaranteed-rent/" />
  <meta property="og:image" content="https://alpeon.fr/assets/images/hero-accueil.jpg" />
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "BreadcrumbList",
        "itemListElement": [
          {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://alpeon.fr/en/accueil/" }},
          {{ "@type": "ListItem", "position": 2, "name": "Guaranteed Rent", "item": "https://alpeon.fr/en/guaranteed-rent/" }}
        ]
      }},
      {{
        "@type": "Service",
        "name": "Guaranteed Rent — ALPÉON",
        "provider": {{ "@type": "Organization", "@id": "https://alpeon.fr/#organization" }},
        "serviceType": "Property management with guaranteed income",
        "description": "ALPÉON pays a fixed monthly rent to property owners regardless of occupancy. Available in Courchevel, Megève, Méribel, Tignes, Val d'Isère and Val Thorens.",
        "areaServed": ["Courchevel", "Megève", "Méribel", "Tignes", "Val d'Isère", "Val Thorens"]
      }},
      {{
        "@type": "FAQPage",
        "mainEntity": [
          {{
            "@type": "Question",
            "name": "What is ALPÉON's guaranteed rent scheme?",
            "acceptedAnswer": {{ "@type": "Answer", "text": "ALPÉON becomes your direct tenant. We pay you a fixed monthly rent whether your property is occupied or not. Zero vacancy risk, guaranteed income." }}
          }},
          {{
            "@type": "Question",
            "name": "How is the guaranteed rent amount calculated?",
            "acceptedAnswer": {{ "@type": "Answer", "text": "The guaranteed rent is calculated based on the property size, location (resort and altitude), quality level, and local seasonality. Our online estimator provides a personalised figure in under 2 minutes." }}
          }},
          {{
            "@type": "Question",
            "name": "Can I still use my property personally?",
            "acceptedAnswer": {{ "@type": "Answer", "text": "Yes. Personal-use blackout periods can be agreed at contract signing. The guaranteed rent is calculated taking these exclusive periods into account." }}
          }},
          {{
            "@type": "Question",
            "name": "In which resorts is guaranteed rent available?",
            "acceptedAnswer": {{ "@type": "Answer", "text": "Available in Courchevel, Megève, Méribel, Tignes, Val d'Isère and Val Thorens — the 6 alpine resorts where ALPÉON manages over 200 properties." }}
          }}
        ]
      }}
    ]
  }}
  </script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Yeseva+One&display=swap" rel="stylesheet" />
  <link href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400;1,500;1,600&display=swap" rel="stylesheet" />

  <style>
  :root {{
    --green: #2C3D30; --green-d: #223028; --gold: #E8CBA0; --gold-d: #D4B48A;
    --ink: #0d1a0f; --white: #FAFEFF;
    --font-sans: 'Poppins', sans-serif; --font-serif: 'Yeseva One', serif;
    --nav-h: 88px; --max: 1380px; --pad: clamp(24px, 5vw, 80px);
  }}
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html {{ scroll-behavior: smooth; -webkit-font-smoothing: antialiased; }}
  body {{ font-family: var(--font-sans); font-weight: 300; background: var(--ink); color: rgba(250,254,255,.85); line-height: 1.6; overflow-x: hidden; }}
  img {{ display: block; max-width: 100%; }}
  a {{ text-decoration: none; color: inherit; }}
  ul {{ list-style: none; }}
  .container {{ width: 100%; max-width: var(--max); margin: 0 auto; padding: 0 var(--pad); }}
  {nav_css}
  .lg-hero {{ padding: calc(var(--nav-h) + 80px) var(--pad) 90px; text-align: center; max-width: 820px; margin: 0 auto; }}
  .lg-eyebrow {{ font-size: .72rem; letter-spacing: .2em; text-transform: uppercase; color: var(--gold); opacity: .8; margin-bottom: 1.5rem; }}
  .lg-hero h1 {{ font-family: var(--font-serif); font-size: clamp(2.2rem, 5vw, 3.8rem); font-weight: 400; line-height: 1.15; margin-bottom: 1.5rem; color: #fff; }}
  .lg-hero h1 em {{ font-style: italic; color: var(--gold); }}
  .lg-hero-sub {{ font-size: 1.05rem; color: rgba(250,254,255,.55); max-width: 560px; margin: 0 auto 2.5rem; line-height: 1.8; }}
  .lg-hero-cta {{ display: inline-flex; align-items: center; gap: .6rem; background: var(--gold); color: var(--ink); padding: .9rem 2rem; border-radius: 4px; font-size: .8rem; font-weight: 600; letter-spacing: .12em; text-transform: uppercase; transition: background .2s; }}
  .lg-hero-cta:hover {{ background: var(--gold-d); }}
  .lg-steps {{ background: rgba(44,61,48,.18); border-top: 1px solid rgba(232,203,160,.06); border-bottom: 1px solid rgba(232,203,160,.06); padding: 80px var(--pad); }}
  .lg-steps-inner {{ max-width: var(--max); margin: 0 auto; }}
  .lg-steps-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 2.5rem; margin-top: 3.5rem; }}
  @media (max-width: 760px) {{ .lg-steps-grid {{ grid-template-columns: 1fr; max-width: 480px; margin-inline: auto; }} }}
  .lg-step {{ padding: 2rem; background: rgba(255,255,255,.04); border: 1px solid rgba(232,203,160,.12); border-radius: 12px; }}
  .lg-step-num {{ width: 44px; height: 44px; border: 1px solid rgba(232,203,160,.3); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-family: var(--font-serif); font-size: 1rem; color: var(--gold); margin-bottom: 1.25rem; }}
  .lg-step h3 {{ font-size: .95rem; font-weight: 500; color: rgba(250,254,255,.9); margin-bottom: .6rem; }}
  .lg-step p {{ font-size: .83rem; color: rgba(250,254,255,.45); line-height: 1.75; }}
  .lg-compare {{ padding: 80px var(--pad); max-width: var(--max); margin: 0 auto; }}
  .lg-compare-table {{ width: 100%; border-collapse: collapse; margin-top: 2.5rem; }}
  .lg-compare-table th, .lg-compare-table td {{ padding: 1rem 1.25rem; text-align: left; border-bottom: 1px solid rgba(232,203,160,.08); font-size: .85rem; }}
  .lg-compare-table thead th {{ font-size: .72rem; letter-spacing: .12em; text-transform: uppercase; color: rgba(250,254,255,.4); font-weight: 400; }}
  .lg-compare-table thead th:nth-child(2) {{ color: var(--gold); }}
  .lg-compare-table td:nth-child(2) {{ color: rgba(250,254,255,.9); }}
  .lg-compare-table td:nth-child(1) {{ color: rgba(250,254,255,.6); }}
  .lg-compare-table td:nth-child(3) {{ color: rgba(250,254,255,.35); }}
  .check {{ color: #7ecb8f; }}
  .cross {{ color: rgba(250,100,100,.6); }}
  .lg-est {{ padding: 80px var(--pad); background: rgba(44,61,48,.25); border-top: 1px solid rgba(232,203,160,.06); text-align: center; }}
  .lg-est-inner {{ max-width: 620px; margin: 0 auto; }}
  .lg-est h2 {{ font-family: var(--font-serif); font-size: clamp(1.6rem, 3.5vw, 2.4rem); color: #fff; margin-bottom: 1rem; }}
  .lg-est h2 em {{ font-style: italic; color: var(--gold); }}
  .lg-est p {{ color: rgba(250,254,255,.5); margin-bottom: 2rem; font-size: .9rem; }}
  .lg-faq {{ padding: 80px var(--pad); max-width: 760px; margin: 0 auto; }}
  .lg-faq h2 {{ font-family: var(--font-serif); font-size: clamp(1.6rem, 3.5vw, 2.2rem); color: #fff; margin-bottom: 2.5rem; }}
  .faq-item {{ border-bottom: 1px solid rgba(232,203,160,.1); }}
  .faq-q {{ width: 100%; background: none; border: none; text-align: left; padding: 1.25rem 0; cursor: pointer; display: flex; justify-content: space-between; align-items: center; gap: 1rem; color: rgba(250,254,255,.9); font-size: .92rem; font-family: var(--font-sans); font-weight: 400; line-height: 1.5; }}
  .faq-icon {{ width: 28px; height: 28px; border: 1px solid rgba(232,203,160,.2); border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }}
  .faq-icon svg {{ width: 12px; height: 12px; stroke: rgba(250,254,255,.6); transition: transform .25s; }}
  .faq-item.open .faq-icon svg {{ transform: rotate(45deg); }}
  .faq-a {{ display: none; padding: 0 0 1.25rem; color: rgba(250,254,255,.45); font-size: .85rem; line-height: 1.75; }}
  .faq-item.open .faq-a {{ display: block; }}
  .lg-cta {{ padding: 90px var(--pad); background: var(--green); text-align: center; }}
  .lg-cta-inner {{ max-width: 640px; margin: 0 auto; }}
  .lg-cta-eyebrow {{ font-size: .72rem; letter-spacing: .2em; text-transform: uppercase; color: rgba(232,203,160,.7); margin-bottom: 1.25rem; }}
  .lg-cta h2 {{ font-family: var(--font-serif); font-size: clamp(1.8rem, 4vw, 2.8rem); color: #fff; margin-bottom: 1rem; }}
  .lg-cta h2 em {{ font-style: italic; color: var(--gold); }}
  .lg-cta p {{ color: rgba(250,254,255,.6); margin-bottom: 2.5rem; font-size: .95rem; }}
  .lg-cta-btns {{ display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; }}
  .btn-primary {{ display: inline-flex; align-items: center; gap: .5rem; background: var(--gold); color: var(--ink); padding: .9rem 2rem; border-radius: 4px; font-size: .8rem; font-weight: 600; letter-spacing: .1em; text-transform: uppercase; transition: background .2s; }}
  .btn-primary:hover {{ background: var(--gold-d); }}
  .btn-ghost {{ display: inline-flex; align-items: center; gap: .5rem; border: 1px solid rgba(232,203,160,.4); color: rgba(250,254,255,.7); padding: .9rem 2rem; border-radius: 4px; font-size: .8rem; font-weight: 500; letter-spacing: .1em; text-transform: uppercase; transition: all .2s; }}
  .btn-ghost:hover {{ border-color: var(--gold); color: var(--gold); }}
  .sec-eyebrow {{ font-size: .72rem; letter-spacing: .2em; text-transform: uppercase; color: var(--gold); opacity: .8; margin-bottom: 1rem; }}
  .sec-title {{ font-family: var(--font-serif); font-size: clamp(1.8rem, 4vw, 2.6rem); font-weight: 400; line-height: 1.2; color: #fff; }}
  .sec-title em {{ font-style: italic; color: var(--gold); }}
  .sec-desc {{ color: rgba(250,254,255,.45); margin-top: .75rem; font-size: .9rem; max-width: 540px; line-height: 1.8; }}
  .breadcrumb {{ padding: .75rem 0; }}
  .breadcrumb-list {{ display: flex; align-items: center; gap: .4rem; list-style: none; flex-wrap: wrap; }}
  .breadcrumb-list li {{ display: flex; align-items: center; gap: .4rem; }}
  .breadcrumb-list li::before {{ content: '›'; color: rgba(250,254,255,.25); font-size: .8rem; }}
  .breadcrumb-list li:first-child::before {{ display: none; }}
  .breadcrumb-list a {{ color: rgba(250,254,255,.35); font-size: .72rem; letter-spacing: .06em; text-transform: uppercase; transition: color .2s; }}
  .breadcrumb-list span {{ color: rgba(250,254,255,.55); font-size: .72rem; letter-spacing: .06em; text-transform: uppercase; }}
  </style>
</head>
<body>
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-PXZ2KXWV" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>

  {header_html}

  <div class="container" style="padding-top: calc(var(--nav-h) + 1rem)">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <ol class="breadcrumb-list">
        <li><a href="/en/accueil/">Home</a></li>
        <li><span>Guaranteed Rent</span></li>
      </ol>
    </nav>
  </div>

  <section style="padding-top:0">
    <div class="lg-hero">
      <div class="lg-eyebrow">Exclusive ALPÉON scheme</div>
      <h1>A fixed <em>guaranteed</em><br>rent every month</h1>
      <p class="lg-hero-sub">Whether your chalet has 20 or 80 booked nights, you receive the same amount. ALPÉON becomes your direct tenant — zero vacancy, zero uncertainty.</p>
      <a href="/en/estimateur/" class="lg-hero-cta">
        Calculate my guaranteed rent
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
      </a>
    </div>
  </section>

  <section class="lg-steps">
    <div class="lg-steps-inner">
      <div class="sec-eyebrow" style="text-align:center">How it works</div>
      <h2 class="sec-title" style="text-align:center;margin-bottom:0">The process in <em>3 steps</em></h2>
      <div class="lg-steps-grid">
        <div class="lg-step">
          <div class="lg-step-num">01</div>
          <h3>Personalised estimate</h3>
          <p>Our estimator calculates your guaranteed rent range in 2 minutes — size, quality level, resort and location.</p>
        </div>
        <div class="lg-step">
          <div class="lg-step-num">02</div>
          <h3>Management agreement</h3>
          <p>ALPÉON becomes your direct tenant. We contractually fix the monthly amount and conditions for the full duration.</p>
        </div>
        <div class="lg-step">
          <div class="lg-step-num">03</div>
          <h3>Monthly guaranteed transfer</h3>
          <p>Every month, on a fixed date, your rent is paid — whether there are 0 or 10 stays that month. Track everything from your owner dashboard.</p>
        </div>
      </div>
    </div>
  </section>

  <section style="background:rgba(44,61,48,.08); border-top:1px solid rgba(232,203,160,.06)">
    <div class="lg-compare">
      <div class="sec-eyebrow">Why choose ALPÉON</div>
      <h2 class="sec-title">Guaranteed rent <em>vs.</em> traditional management</h2>
      <p class="sec-desc">The fundamental difference: with ALPÉON, your income no longer depends on travellers.</p>
      <table class="lg-compare-table">
        <thead>
          <tr><th>Criteria</th><th>ALPÉON guaranteed rent</th><th>Traditional management</th></tr>
        </thead>
        <tbody>
          <tr><td>Monthly income</td><td><span class="check">✓</span> Fixed and contractual</td><td><span class="cross">✗</span> Variable by occupancy</td></tr>
          <tr><td>Vacancy periods</td><td><span class="check">✓</span> No impact on income</td><td><span class="cross">✗</span> Empty weeks = zero income</td></tr>
          <tr><td>Operations</td><td><span class="check">✓</span> Fully managed</td><td><span class="cross">✗</span> Partial coordination</td></tr>
          <tr><td>Transparency</td><td><span class="check">✓</span> Owner dashboard</td><td><span class="cross">✗</span> Often monthly reporting only</td></tr>
          <tr><td>Personal stays</td><td><span class="check">✓</span> Plannable at signing</td><td>Subject to availability</td></tr>
          <tr><td>Routine maintenance</td><td><span class="check">✓</span> Included in contract</td><td>Depends on package</td></tr>
        </tbody>
      </table>
    </div>
  </section>

  <section class="lg-est">
    <div class="lg-est-inner">
      <div class="sec-eyebrow">Free estimator</div>
      <h2>How much does your property earn <em>with ALPÉON</em>?</h2>
      <p>Get a personalised range in under 2 minutes. Free, no commitment.</p>
      <a href="/en/estimateur/" class="lg-hero-cta">
        Run the estimate
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
      </a>
    </div>
  </section>

  <section style="background:rgba(44,61,48,.12)">
    <div class="lg-faq">
      <h2>Frequently asked questions about <em style="font-style:italic;color:var(--gold)">guaranteed rent</em></h2>
      <div class="faq-item">
        <button class="faq-q" onclick="this.parentElement.classList.toggle('open')">
          What is ALPÉON's guaranteed rent scheme?
          <span class="faq-icon"><svg viewBox="0 0 24 24" fill="none" stroke-width="2.5"><path d="M12 5v14M5 12h14"/></svg></span>
        </button>
        <p class="faq-a">ALPÉON becomes your direct tenant. We pay you a fixed monthly rent whether your property is occupied or not. Zero vacancy risk, guaranteed income.</p>
      </div>
      <div class="faq-item">
        <button class="faq-q" onclick="this.parentElement.classList.toggle('open')">
          How is the guaranteed rent amount calculated?
          <span class="faq-icon"><svg viewBox="0 0 24 24" fill="none" stroke-width="2.5"><path d="M12 5v14M5 12h14"/></svg></span>
        </button>
        <p class="faq-a">The guaranteed rent is based on property size, resort and altitude, quality level, and local seasonality. Our online estimator provides a personalised figure in under 2 minutes.</p>
      </div>
      <div class="faq-item">
        <button class="faq-q" onclick="this.parentElement.classList.toggle('open')">
          Can I still use my property personally?
          <span class="faq-icon"><svg viewBox="0 0 24 24" fill="none" stroke-width="2.5"><path d="M12 5v14M5 12h14"/></svg></span>
        </button>
        <p class="faq-a">Yes. Personal-use blackout periods can be agreed at contract signing. The guaranteed rent is calculated taking these exclusive periods into account.</p>
      </div>
      <div class="faq-item">
        <button class="faq-q" onclick="this.parentElement.classList.toggle('open')">
          In which resorts is guaranteed rent available?
          <span class="faq-icon"><svg viewBox="0 0 24 24" fill="none" stroke-width="2.5"><path d="M12 5v14M5 12h14"/></svg></span>
        </button>
        <p class="faq-a">Available in Courchevel, Megève, Méribel, Tignes, Val d'Isère and Val Thorens — the 6 alpine resorts where ALPÉON manages over 200 properties.</p>
      </div>
    </div>
  </section>

  <section class="lg-cta">
    <div class="lg-cta-inner">
      <div class="lg-cta-eyebrow">Own an alpine property?</div>
      <h2>Your property deserves <em>guaranteed income</em></h2>
      <p>Join ALPÉON property owners who receive a fixed monthly rent, effortlessly.</p>
      <div class="lg-cta-btns">
        <a href="/en/estimateur/" class="btn-primary">Estimate my guaranteed rent</a>
        <a href="/en/contact/" class="btn-ghost">Talk to an expert</a>
      </div>
    </div>
  </section>

  {EN_FOOTER}

<script>
(function(){{
  var h=document.getElementById('site-header');
  if(!h)return;
  function u(){{h.classList.toggle('scrolled',window.scrollY>40);}}
  window.addEventListener('scroll',u,{{passive:true}});
  u();
}})();
async function submitNewsletter(e){{
  e.preventDefault();
  document.getElementById('nl-msg').textContent='Thank you! You are subscribed.';
}}
</script>
</body>
</html>'''

os.makedirs(f'{BASE}/en/guaranteed-rent', exist_ok=True)
with open(f'{BASE}/en/guaranteed-rent/index.html', 'w', encoding='utf-8') as f:
    f.write(EN_HTML)
print('Created: en/guaranteed-rent/index.html')