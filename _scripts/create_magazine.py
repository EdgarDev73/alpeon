#!/usr/bin/env python3
"""
Create /magazine/ (FR) and /en/magazine/ (EN) scaffold pages.
Extracts nav/footer from proprietaires/index.html for consistency.
"""
import os

BASE = '/Users/edgarvernet/claude/alpeon'

with open(f'{BASE}/proprietaires/index.html', 'r', encoding='utf-8') as f:
    prop = f.read()

# Extract nav CSS block
nav_start = prop.find('/* @@NAV-START@@ */')
nav_end = prop.find('/* @@NAV-END@@ */') + len('/* @@NAV-END@@ */')
nav_css = prop[nav_start:nav_end]

# Extract header HTML
header_start = prop.find('<header class="site-header"')
header_end = prop.find('</header>') + len('</header>')
header_html = prop[header_start:header_end]

# Extract footer HTML
footer_html = prop[prop.find('<!-- FOOTER -->'):]

JS_BLOCK = '''<script>
(function(){
  var h=document.getElementById('site-header');
  if(!h)return;
  function u(){h.classList.toggle('scrolled',window.scrollY>40);}
  window.addEventListener('scroll',u,{passive:true});
  u();
})();
(function(){
  var wrap=document.getElementById('hdr-lang-wrap');
  var drop=document.getElementById('hdr-lang-dropdown');
  if(!wrap||!drop)return;
  var links=document.querySelectorAll('.site-lang a');
  links.forEach(function(a){
    var item=document.createElement('a');
    item.href=a.href;
    item.className='hdr-lang-item'+(a.classList.contains('active')?' active':'');
    item.textContent=a.textContent.trim();
    drop.appendChild(item);
  });
  document.addEventListener('click',function(e){if(!wrap.contains(e.target))wrap.classList.remove('open');});
})();
function toggleLangDropdown(){
  var wrap=document.getElementById('hdr-lang-wrap');
  if(!wrap)return;
  wrap.classList.toggle('open');
}
async function submitNewsletter(e){
  e.preventDefault();
  const email=document.getElementById('nl-email').value;
  document.getElementById('nl-msg').textContent='Merci ! Vous êtes inscrit.';
}
</script>'''

# ── FR MAGAZINE PAGE ──
FR_HTML = f'''<!DOCTYPE html>
<html lang="fr">
<head>
  <!-- Consent Mode v2 — RGPD -->
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
  <title>Magazine — Investir, Gérer, Vivre en Station | ALPÉON</title>
  <meta name="description" content="Conseils d'experts pour propriétaires de biens alpins : investissement en station, fiscalité LMNP, gestion locative, saisonnalité. Le magazine ALPÉON." />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="https://alpeon.fr/magazine/" />
  <link rel="alternate" hreflang="fr" href="https://alpeon.fr/magazine/" />
  <link rel="alternate" hreflang="en" href="https://alpeon.fr/en/magazine/" />
  <link rel="alternate" hreflang="x-default" href="https://alpeon.fr/magazine/" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="Magazine ALPÉON — Investir et Gérer un Bien Alpin" />
  <meta property="og:description" content="Conseils d'experts pour propriétaires de biens alpins : investissement en station, fiscalité LMNP, gestion locative." />
  <meta property="og:url" content="https://alpeon.fr/magazine/" />
  <meta property="og:image" content="https://alpeon.fr/assets/images/hero-accueil.jpg" />
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "BreadcrumbList",
        "itemListElement": [
          {{ "@type": "ListItem", "position": 1, "name": "Accueil", "item": "https://alpeon.fr/accueil/" }},
          {{ "@type": "ListItem", "position": 2, "name": "Magazine", "item": "https://alpeon.fr/magazine/" }}
        ]
      }},
      {{
        "@type": "Blog",
        "@id": "https://alpeon.fr/magazine/",
        "name": "Magazine ALPÉON",
        "description": "Conseils d'experts pour propriétaires de biens alpins : investissement, fiscalité, gestion locative.",
        "publisher": {{ "@type": "Organization", "@id": "https://alpeon.fr/#organization" }},
        "inLanguage": "fr",
        "url": "https://alpeon.fr/magazine/"
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

  /* ── Breadcrumb ── */
  .breadcrumb {{ padding: .75rem 0; }}
  .breadcrumb-list {{ display: flex; align-items: center; gap: .4rem; list-style: none; flex-wrap: wrap; }}
  .breadcrumb-list li {{ display: flex; align-items: center; gap: .4rem; }}
  .breadcrumb-list li::before {{ content: '›'; color: rgba(250,254,255,.25); font-size: .8rem; }}
  .breadcrumb-list li:first-child::before {{ display: none; }}
  .breadcrumb-list a {{ color: rgba(250,254,255,.35); font-size: .72rem; letter-spacing: .06em; text-transform: uppercase; transition: color .2s; }}
  .breadcrumb-list a:hover {{ color: var(--gold); }}
  .breadcrumb-list span {{ color: rgba(250,254,255,.55); font-size: .72rem; letter-spacing: .06em; text-transform: uppercase; }}

  /* ── Magazine hero ── */
  .mag-hero {{ padding: calc(var(--nav-h) + 80px) var(--pad) 70px; text-align: center; max-width: 720px; margin: 0 auto; }}
  .mag-eyebrow {{ font-size: .72rem; letter-spacing: .2em; text-transform: uppercase; color: var(--gold); opacity: .8; margin-bottom: 1.5rem; }}
  .mag-hero h1 {{ font-family: var(--font-serif); font-size: clamp(2rem, 4.5vw, 3.4rem); font-weight: 400; line-height: 1.2; color: #fff; margin-bottom: 1rem; }}
  .mag-hero h1 em {{ font-style: italic; color: var(--gold); }}
  .mag-hero-sub {{ font-size: .95rem; color: rgba(250,254,255,.5); max-width: 520px; margin: 0 auto; line-height: 1.8; }}

  /* ── Categories ── */
  .mag-cats {{ padding: 0 var(--pad) 50px; max-width: var(--max); margin: 0 auto; display: flex; gap: .6rem; flex-wrap: wrap; justify-content: center; }}
  .mag-cat {{ display: inline-flex; align-items: center; padding: .45rem 1.1rem; border: 1px solid rgba(232,203,160,.18); border-radius: 100px; font-size: .72rem; letter-spacing: .1em; text-transform: uppercase; color: rgba(250,254,255,.5); cursor: pointer; transition: all .2s; }}
  .mag-cat:hover, .mag-cat.active {{ border-color: var(--gold); color: var(--gold); }}

  /* ── Articles grid ── */
  .mag-grid-wrap {{ padding: 0 var(--pad) 80px; max-width: var(--max); margin: 0 auto; }}
  .mag-section-title {{ font-family: var(--font-serif); font-size: clamp(1.2rem, 2.5vw, 1.6rem); color: #fff; margin-bottom: 2rem; padding-bottom: .75rem; border-bottom: 1px solid rgba(232,203,160,.1); }}
  .mag-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; margin-bottom: 3.5rem; }}
  @media (max-width: 900px) {{ .mag-grid {{ grid-template-columns: repeat(2, 1fr); }} }}
  @media (max-width: 580px) {{ .mag-grid {{ grid-template-columns: 1fr; }} }}

  /* ── Article card ── */
  .mag-card {{ display: flex; flex-direction: column; border: 1px solid rgba(232,203,160,.1); border-radius: 10px; overflow: hidden; background: rgba(255,255,255,.03); transition: border-color .2s, transform .2s; }}
  .mag-card:hover {{ border-color: rgba(232,203,160,.25); transform: translateY(-3px); }}
  .mag-card-img {{ aspect-ratio: 16/9; background: rgba(44,61,48,.4); position: relative; overflow: hidden; display: flex; align-items: center; justify-content: center; }}
  .mag-card-img-placeholder {{ font-size: .75rem; letter-spacing: .1em; text-transform: uppercase; color: rgba(232,203,160,.3); }}
  .mag-card-body {{ padding: 1.25rem; flex: 1; display: flex; flex-direction: column; }}
  .mag-card-cat {{ font-size: .65rem; letter-spacing: .15em; text-transform: uppercase; color: var(--gold); opacity: .75; margin-bottom: .6rem; }}
  .mag-card-title {{ font-size: .95rem; font-weight: 500; color: rgba(250,254,255,.9); line-height: 1.45; margin-bottom: .6rem; flex: 1; }}
  .mag-card-meta {{ display: flex; align-items: center; gap: .8rem; margin-top: .75rem; font-size: .72rem; color: rgba(250,254,255,.3); }}
  .mag-card-todo {{ display: inline-block; font-size: .65rem; letter-spacing: .08em; text-transform: uppercase; padding: .25rem .7rem; border: 1px dashed rgba(232,203,160,.2); border-radius: 4px; color: rgba(232,203,160,.4); margin-top: .75rem; }}

  /* ── CTA ── */
  .mag-cta {{ padding: 80px var(--pad); background: var(--green); text-align: center; }}
  .mag-cta-inner {{ max-width: 580px; margin: 0 auto; }}
  .mag-cta h2 {{ font-family: var(--font-serif); font-size: clamp(1.6rem, 3.5vw, 2.4rem); color: #fff; margin-bottom: 1rem; }}
  .mag-cta h2 em {{ font-style: italic; color: var(--gold); }}
  .mag-cta p {{ color: rgba(250,254,255,.55); margin-bottom: 2rem; font-size: .9rem; }}
  .btn-gold {{ display: inline-flex; align-items: center; gap: .5rem; background: var(--gold); color: var(--ink); padding: .9rem 2rem; border-radius: 4px; font-size: .8rem; font-weight: 600; letter-spacing: .1em; text-transform: uppercase; transition: background .2s; }}
  .btn-gold:hover {{ background: var(--gold-d); }}
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
        <li><span>Magazine</span></li>
      </ol>
    </nav>
  </div>

  <!-- HERO -->
  <section style="padding-top:0">
    <div class="mag-hero">
      <div class="mag-eyebrow">Conseils &amp; ressources</div>
      <h1>Le magazine des <em>propriétaires alpins</em></h1>
      <p class="mag-hero-sub">Investissement en station, fiscalité LMNP, gestion locative, vie d'opérateur. Des articles rédigés par les experts ALPÉON.</p>
    </div>
  </section>

  <!-- CATEGORIES -->
  <div class="mag-cats">
    <span class="mag-cat active">Tous</span>
    <span class="mag-cat">Investir en station</span>
    <span class="mag-cat">Fiscalité LMNP</span>
    <span class="mag-cat">Stations</span>
    <span class="mag-cat">Vie d'opérateur</span>
  </div>

  <!-- ARTICLES GRID -->
  <div class="mag-grid-wrap">

    <h2 class="mag-section-title">Investir en station</h2>
    <div class="mag-grid">
      <article class="mag-card">
        <div class="mag-card-img"><span class="mag-card-img-placeholder">Image à venir</span></div>
        <div class="mag-card-body">
          <div class="mag-card-cat">Investir en station</div>
          <h3 class="mag-card-title">Investir à Courchevel en 2025 : les prix, les rendements, les pièges à éviter</h3>
          <div class="mag-card-meta"><span>5 min</span><span>·</span><span>Équipe ALPÉON</span></div>
          <!-- TODO: Rédiger le contenu complet de cet article -->
          <span class="mag-card-todo">Article à rédiger</span>
        </div>
      </article>
      <article class="mag-card">
        <div class="mag-card-img"><span class="mag-card-img-placeholder">Image à venir</span></div>
        <div class="mag-card-body">
          <div class="mag-card-cat">Investir en station</div>
          <h3 class="mag-card-title">Val d'Isère vs. Méribel : quel marché offre le meilleur rendement locatif ?</h3>
          <div class="mag-card-meta"><span>7 min</span><span>·</span><span>Équipe ALPÉON</span></div>
          <!-- TODO: Rédiger le contenu complet de cet article -->
          <span class="mag-card-todo">Article à rédiger</span>
        </div>
      </article>
      <article class="mag-card">
        <div class="mag-card-img"><span class="mag-card-img-placeholder">Image à venir</span></div>
        <div class="mag-card-body">
          <div class="mag-card-cat">Investir en station</div>
          <h3 class="mag-card-title">Neuf ou ancien en station de ski : ce que les chiffres disent vraiment</h3>
          <div class="mag-card-meta"><span>6 min</span><span>·</span><span>Équipe ALPÉON</span></div>
          <!-- TODO: Rédiger le contenu complet de cet article -->
          <span class="mag-card-todo">Article à rédiger</span>
        </div>
      </article>
    </div>

    <h2 class="mag-section-title">Fiscalité LMNP</h2>
    <div class="mag-grid">
      <article class="mag-card">
        <div class="mag-card-img"><span class="mag-card-img-placeholder">Image à venir</span></div>
        <div class="mag-card-body">
          <div class="mag-card-cat">Fiscalité LMNP</div>
          <h3 class="mag-card-title">LMNP en 2025 : guide complet pour les propriétaires de biens alpins</h3>
          <div class="mag-card-meta"><span>10 min</span><span>·</span><span>Équipe ALPÉON</span></div>
          <!-- TODO: Rédiger le contenu complet de cet article -->
          <span class="mag-card-todo">Article à rédiger</span>
        </div>
      </article>
      <article class="mag-card">
        <div class="mag-card-img"><span class="mag-card-img-placeholder">Image à venir</span></div>
        <div class="mag-card-body">
          <div class="mag-card-cat">Fiscalité LMNP</div>
          <h3 class="mag-card-title">Amortissement LMNP : comment optimiser la fiscalité de votre chalet</h3>
          <div class="mag-card-meta"><span>8 min</span><span>·</span><span>Équipe ALPÉON</span></div>
          <!-- TODO: Rédiger le contenu complet de cet article -->
          <span class="mag-card-todo">Article à rédiger</span>
        </div>
      </article>
      <article class="mag-card">
        <div class="mag-card-img"><span class="mag-card-img-placeholder">Image à venir</span></div>
        <div class="mag-card-body">
          <div class="mag-card-cat">Fiscalité LMNP</div>
          <h3 class="mag-card-title">Micro-BIC vs. régime réel : quel choix pour un bien de station haut de gamme ?</h3>
          <div class="mag-card-meta"><span>6 min</span><span>·</span><span>Équipe ALPÉON</span></div>
          <!-- TODO: Rédiger le contenu complet de cet article -->
          <span class="mag-card-todo">Article à rédiger</span>
        </div>
      </article>
    </div>

    <h2 class="mag-section-title">Stations</h2>
    <div class="mag-grid">
      <article class="mag-card">
        <div class="mag-card-img"><span class="mag-card-img-placeholder">Image à venir</span></div>
        <div class="mag-card-body">
          <div class="mag-card-cat">Stations</div>
          <h3 class="mag-card-title">Tignes : pourquoi la saison 2024-2025 a surpassé les attentes des propriétaires</h3>
          <div class="mag-card-meta"><span>5 min</span><span>·</span><span>Équipe ALPÉON</span></div>
          <!-- TODO: Rédiger le contenu complet de cet article -->
          <span class="mag-card-todo">Article à rédiger</span>
        </div>
      </article>
      <article class="mag-card">
        <div class="mag-card-img"><span class="mag-card-img-placeholder">Image à venir</span></div>
        <div class="mag-card-body">
          <div class="mag-card-cat">Stations</div>
          <h3 class="mag-card-title">Megève hors-saison : la demande estivale qui change la donne pour les propriétaires</h3>
          <div class="mag-card-meta"><span>5 min</span><span>·</span><span>Équipe ALPÉON</span></div>
          <!-- TODO: Rédiger le contenu complet de cet article -->
          <span class="mag-card-todo">Article à rédiger</span>
        </div>
      </article>
      <article class="mag-card">
        <div class="mag-card-img"><span class="mag-card-img-placeholder">Image à venir</span></div>
        <div class="mag-card-body">
          <div class="mag-card-cat">Stations</div>
          <h3 class="mag-card-title">Val Thorens en été : une opportunité de diversification pour les propriétaires d'altitude</h3>
          <div class="mag-card-meta"><span>4 min</span><span>·</span><span>Équipe ALPÉON</span></div>
          <!-- TODO: Rédiger le contenu complet de cet article -->
          <span class="mag-card-todo">Article à rédiger</span>
        </div>
      </article>
    </div>

    <h2 class="mag-section-title">Vie d'opérateur</h2>
    <div class="mag-grid">
      <article class="mag-card">
        <div class="mag-card-img"><span class="mag-card-img-placeholder">Image à venir</span></div>
        <div class="mag-card-body">
          <div class="mag-card-cat">Vie d'opérateur</div>
          <h3 class="mag-card-title">Comment ALPÉON coordonne 200+ propriétés sur 6 stations pendant la haute saison</h3>
          <div class="mag-card-meta"><span>8 min</span><span>·</span><span>Équipe ALPÉON</span></div>
          <!-- TODO: Rédiger le contenu complet de cet article -->
          <span class="mag-card-todo">Article à rédiger</span>
        </div>
      </article>
      <article class="mag-card">
        <div class="mag-card-img"><span class="mag-card-img-placeholder">Image à venir</span></div>
        <div class="mag-card-body">
          <div class="mag-card-cat">Vie d'opérateur</div>
          <h3 class="mag-card-title">Tarification dynamique en station : comment maximiser le RevPAR sur un chalet haut de gamme</h3>
          <div class="mag-card-meta"><span>7 min</span><span>·</span><span>Équipe ALPÉON</span></div>
          <!-- TODO: Rédiger le contenu complet de cet article -->
          <span class="mag-card-todo">Article à rédiger</span>
        </div>
      </article>
      <article class="mag-card">
        <div class="mag-card-img"><span class="mag-card-img-placeholder">Image à venir</span></div>
        <div class="mag-card-body">
          <div class="mag-card-cat">Vie d'opérateur</div>
          <h3 class="mag-card-title">Loyer garanti vs. commission : les questions que tout propriétaire doit se poser</h3>
          <div class="mag-card-meta"><span>6 min</span><span>·</span><span>Équipe ALPÉON</span></div>
          <!-- TODO: Rédiger le contenu complet de cet article -->
          <span class="mag-card-todo">Article à rédiger</span>
        </div>
      </article>
    </div>

  </div>

  <!-- CTA -->
  <section class="mag-cta">
    <div class="mag-cta-inner">
      <div style="font-size:.72rem;letter-spacing:.2em;text-transform:uppercase;color:rgba(232,203,160,.7);margin-bottom:1.25rem">Propriétaire d'un bien alpin</div>
      <h2>Estimez vos <em>revenus locatifs</em></h2>
      <p>Calculez ce que votre chalet ou appartement alpin peut générer avec ALPÉON. Gratuit, sans engagement, en 2 minutes.</p>
      <a href="/estimateur/" class="btn-gold">
        Lancer l'estimation
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
      </a>
    </div>
  </section>

  {footer_html}

{JS_BLOCK}
</body>
</html>'''

# ── EN MAGAZINE PAGE ──
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
  <title>Magazine — Invest, Manage, Live in an Alpine Resort | ALPÉON</title>
  <meta name="description" content="Expert advice for alpine property owners: ski resort investment, LMNP tax, property management, operator insights. The ALPÉON Magazine." />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="https://alpeon.fr/en/magazine/" />
  <link rel="alternate" hreflang="en" href="https://alpeon.fr/en/magazine/" />
  <link rel="alternate" hreflang="fr" href="https://alpeon.fr/magazine/" />
  <link rel="alternate" hreflang="x-default" href="https://alpeon.fr/magazine/" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="ALPÉON Magazine — Invest and Manage an Alpine Property" />
  <meta property="og:description" content="Expert advice for alpine property owners: ski resort investment, tax optimisation, property management." />
  <meta property="og:url" content="https://alpeon.fr/en/magazine/" />
  <meta property="og:image" content="https://alpeon.fr/assets/images/hero-accueil.jpg" />
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "BreadcrumbList",
        "itemListElement": [
          {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://alpeon.fr/en/accueil/" }},
          {{ "@type": "ListItem", "position": 2, "name": "Magazine", "item": "https://alpeon.fr/en/magazine/" }}
        ]
      }},
      {{
        "@type": "Blog",
        "@id": "https://alpeon.fr/en/magazine/",
        "name": "ALPÉON Magazine",
        "description": "Expert advice for alpine property owners: investment, tax, rental management.",
        "publisher": {{ "@type": "Organization", "@id": "https://alpeon.fr/#organization" }},
        "inLanguage": "en",
        "url": "https://alpeon.fr/en/magazine/"
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
  .breadcrumb {{ padding: .75rem 0; }}
  .breadcrumb-list {{ display: flex; align-items: center; gap: .4rem; list-style: none; flex-wrap: wrap; }}
  .breadcrumb-list li {{ display: flex; align-items: center; gap: .4rem; }}
  .breadcrumb-list li::before {{ content: '›'; color: rgba(250,254,255,.25); font-size: .8rem; }}
  .breadcrumb-list li:first-child::before {{ display: none; }}
  .breadcrumb-list a {{ color: rgba(250,254,255,.35); font-size: .72rem; letter-spacing: .06em; text-transform: uppercase; transition: color .2s; }}
  .breadcrumb-list span {{ color: rgba(250,254,255,.55); font-size: .72rem; letter-spacing: .06em; text-transform: uppercase; }}
  .mag-hero {{ padding: calc(var(--nav-h) + 80px) var(--pad) 70px; text-align: center; max-width: 720px; margin: 0 auto; }}
  .mag-eyebrow {{ font-size: .72rem; letter-spacing: .2em; text-transform: uppercase; color: var(--gold); opacity: .8; margin-bottom: 1.5rem; }}
  .mag-hero h1 {{ font-family: var(--font-serif); font-size: clamp(2rem, 4.5vw, 3.4rem); font-weight: 400; line-height: 1.2; color: #fff; margin-bottom: 1rem; }}
  .mag-hero h1 em {{ font-style: italic; color: var(--gold); }}
  .mag-hero-sub {{ font-size: .95rem; color: rgba(250,254,255,.5); max-width: 520px; margin: 0 auto; line-height: 1.8; }}
  .mag-cats {{ padding: 0 var(--pad) 50px; max-width: var(--max); margin: 0 auto; display: flex; gap: .6rem; flex-wrap: wrap; justify-content: center; }}
  .mag-cat {{ display: inline-flex; align-items: center; padding: .45rem 1.1rem; border: 1px solid rgba(232,203,160,.18); border-radius: 100px; font-size: .72rem; letter-spacing: .1em; text-transform: uppercase; color: rgba(250,254,255,.5); cursor: pointer; transition: all .2s; }}
  .mag-cat:hover, .mag-cat.active {{ border-color: var(--gold); color: var(--gold); }}
  .mag-grid-wrap {{ padding: 0 var(--pad) 80px; max-width: var(--max); margin: 0 auto; }}
  .mag-section-title {{ font-family: var(--font-serif); font-size: clamp(1.2rem, 2.5vw, 1.6rem); color: #fff; margin-bottom: 2rem; padding-bottom: .75rem; border-bottom: 1px solid rgba(232,203,160,.1); }}
  .mag-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; margin-bottom: 3.5rem; }}
  @media (max-width: 900px) {{ .mag-grid {{ grid-template-columns: repeat(2, 1fr); }} }}
  @media (max-width: 580px) {{ .mag-grid {{ grid-template-columns: 1fr; }} }}
  .mag-card {{ display: flex; flex-direction: column; border: 1px solid rgba(232,203,160,.1); border-radius: 10px; overflow: hidden; background: rgba(255,255,255,.03); transition: border-color .2s, transform .2s; }}
  .mag-card:hover {{ border-color: rgba(232,203,160,.25); transform: translateY(-3px); }}
  .mag-card-img {{ aspect-ratio: 16/9; background: rgba(44,61,48,.4); display: flex; align-items: center; justify-content: center; }}
  .mag-card-img-placeholder {{ font-size: .75rem; letter-spacing: .1em; text-transform: uppercase; color: rgba(232,203,160,.3); }}
  .mag-card-body {{ padding: 1.25rem; flex: 1; display: flex; flex-direction: column; }}
  .mag-card-cat {{ font-size: .65rem; letter-spacing: .15em; text-transform: uppercase; color: var(--gold); opacity: .75; margin-bottom: .6rem; }}
  .mag-card-title {{ font-size: .95rem; font-weight: 500; color: rgba(250,254,255,.9); line-height: 1.45; margin-bottom: .6rem; flex: 1; }}
  .mag-card-meta {{ display: flex; align-items: center; gap: .8rem; margin-top: .75rem; font-size: .72rem; color: rgba(250,254,255,.3); }}
  .mag-card-todo {{ display: inline-block; font-size: .65rem; letter-spacing: .08em; text-transform: uppercase; padding: .25rem .7rem; border: 1px dashed rgba(232,203,160,.2); border-radius: 4px; color: rgba(232,203,160,.4); margin-top: .75rem; }}
  .mag-cta {{ padding: 80px var(--pad); background: var(--green); text-align: center; }}
  .mag-cta-inner {{ max-width: 580px; margin: 0 auto; }}
  .mag-cta h2 {{ font-family: var(--font-serif); font-size: clamp(1.6rem, 3.5vw, 2.4rem); color: #fff; margin-bottom: 1rem; }}
  .mag-cta h2 em {{ font-style: italic; color: var(--gold); }}
  .mag-cta p {{ color: rgba(250,254,255,.55); margin-bottom: 2rem; font-size: .9rem; }}
  .btn-gold {{ display: inline-flex; align-items: center; gap: .5rem; background: var(--gold); color: var(--ink); padding: .9rem 2rem; border-radius: 4px; font-size: .8rem; font-weight: 600; letter-spacing: .1em; text-transform: uppercase; transition: background .2s; }}
  .btn-gold:hover {{ background: var(--gold-d); }}
  </style>
</head>
<body>
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-PXZ2KXWV" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>

  {header_html}

  <div class="container" style="padding-top: calc(var(--nav-h) + 1rem)">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <ol class="breadcrumb-list">
        <li><a href="/en/accueil/">Home</a></li>
        <li><span>Magazine</span></li>
      </ol>
    </nav>
  </div>

  <section style="padding-top:0">
    <div class="mag-hero">
      <div class="mag-eyebrow">Advice &amp; resources</div>
      <h1>The magazine for <em>alpine property owners</em></h1>
      <p class="mag-hero-sub">Resort investment, LMNP tax, rental management, operator insights. Articles written by ALPÉON's experts.</p>
    </div>
  </section>

  <div class="mag-cats">
    <span class="mag-cat active">All</span>
    <span class="mag-cat">Investing in resorts</span>
    <span class="mag-cat">LMNP Tax</span>
    <span class="mag-cat">Resorts</span>
    <span class="mag-cat">Operator insights</span>
  </div>

  <div class="mag-grid-wrap">

    <h2 class="mag-section-title">Investing in resorts</h2>
    <div class="mag-grid">
      <article class="mag-card">
        <div class="mag-card-img"><span class="mag-card-img-placeholder">Image coming soon</span></div>
        <div class="mag-card-body">
          <div class="mag-card-cat">Investing in resorts</div>
          <h3 class="mag-card-title">Investing in Courchevel in 2025: prices, yields and pitfalls to avoid</h3>
          <div class="mag-card-meta"><span>5 min</span><span>·</span><span>ALPÉON Team</span></div>
          <!-- TODO: Write full article content -->
          <span class="mag-card-todo">Article to be written</span>
        </div>
      </article>
      <article class="mag-card">
        <div class="mag-card-img"><span class="mag-card-img-placeholder">Image coming soon</span></div>
        <div class="mag-card-body">
          <div class="mag-card-cat">Investing in resorts</div>
          <h3 class="mag-card-title">Val d'Isère vs. Méribel: which market offers the best rental yield?</h3>
          <div class="mag-card-meta"><span>7 min</span><span>·</span><span>ALPÉON Team</span></div>
          <!-- TODO: Write full article content -->
          <span class="mag-card-todo">Article to be written</span>
        </div>
      </article>
      <article class="mag-card">
        <div class="mag-card-img"><span class="mag-card-img-placeholder">Image coming soon</span></div>
        <div class="mag-card-body">
          <div class="mag-card-cat">Investing in resorts</div>
          <h3 class="mag-card-title">New-build vs. resale in ski resorts: what the numbers really show</h3>
          <div class="mag-card-meta"><span>6 min</span><span>·</span><span>ALPÉON Team</span></div>
          <!-- TODO: Write full article content -->
          <span class="mag-card-todo">Article to be written</span>
        </div>
      </article>
    </div>

    <h2 class="mag-section-title">LMNP Tax</h2>
    <div class="mag-grid">
      <article class="mag-card">
        <div class="mag-card-img"><span class="mag-card-img-placeholder">Image coming soon</span></div>
        <div class="mag-card-body">
          <div class="mag-card-cat">LMNP Tax</div>
          <h3 class="mag-card-title">LMNP in 2025: the complete guide for alpine property owners</h3>
          <div class="mag-card-meta"><span>10 min</span><span>·</span><span>ALPÉON Team</span></div>
          <!-- TODO: Write full article content -->
          <span class="mag-card-todo">Article to be written</span>
        </div>
      </article>
      <article class="mag-card">
        <div class="mag-card-img"><span class="mag-card-img-placeholder">Image coming soon</span></div>
        <div class="mag-card-body">
          <div class="mag-card-cat">LMNP Tax</div>
          <h3 class="mag-card-title">LMNP depreciation: how to optimise the tax position of your chalet</h3>
          <div class="mag-card-meta"><span>8 min</span><span>·</span><span>ALPÉON Team</span></div>
          <!-- TODO: Write full article content -->
          <span class="mag-card-todo">Article to be written</span>
        </div>
      </article>
      <article class="mag-card">
        <div class="mag-card-img"><span class="mag-card-img-placeholder">Image coming soon</span></div>
        <div class="mag-card-body">
          <div class="mag-card-cat">LMNP Tax</div>
          <h3 class="mag-card-title">Micro-BIC vs. real regime: which is right for a premium ski property?</h3>
          <div class="mag-card-meta"><span>6 min</span><span>·</span><span>ALPÉON Team</span></div>
          <!-- TODO: Write full article content -->
          <span class="mag-card-todo">Article to be written</span>
        </div>
      </article>
    </div>

    <h2 class="mag-section-title">Resorts</h2>
    <div class="mag-grid">
      <article class="mag-card">
        <div class="mag-card-img"><span class="mag-card-img-placeholder">Image coming soon</span></div>
        <div class="mag-card-body">
          <div class="mag-card-cat">Resorts</div>
          <h3 class="mag-card-title">Tignes: why the 2024–2025 season exceeded property owner expectations</h3>
          <div class="mag-card-meta"><span>5 min</span><span>·</span><span>ALPÉON Team</span></div>
          <!-- TODO: Write full article content -->
          <span class="mag-card-todo">Article to be written</span>
        </div>
      </article>
      <article class="mag-card">
        <div class="mag-card-img"><span class="mag-card-img-placeholder">Image coming soon</span></div>
        <div class="mag-card-body">
          <div class="mag-card-cat">Resorts</div>
          <h3 class="mag-card-title">Megève off-season: the summer demand that's changing the game for property owners</h3>
          <div class="mag-card-meta"><span>5 min</span><span>·</span><span>ALPÉON Team</span></div>
          <!-- TODO: Write full article content -->
          <span class="mag-card-todo">Article to be written</span>
        </div>
      </article>
      <article class="mag-card">
        <div class="mag-card-img"><span class="mag-card-img-placeholder">Image coming soon</span></div>
        <div class="mag-card-body">
          <div class="mag-card-cat">Resorts</div>
          <h3 class="mag-card-title">Val Thorens in summer: a diversification opportunity for high-altitude property owners</h3>
          <div class="mag-card-meta"><span>4 min</span><span>·</span><span>ALPÉON Team</span></div>
          <!-- TODO: Write full article content -->
          <span class="mag-card-todo">Article to be written</span>
        </div>
      </article>
    </div>

    <h2 class="mag-section-title">Operator insights</h2>
    <div class="mag-grid">
      <article class="mag-card">
        <div class="mag-card-img"><span class="mag-card-img-placeholder">Image coming soon</span></div>
        <div class="mag-card-body">
          <div class="mag-card-cat">Operator insights</div>
          <h3 class="mag-card-title">How ALPÉON coordinates 200+ properties across 6 resorts during peak season</h3>
          <div class="mag-card-meta"><span>8 min</span><span>·</span><span>ALPÉON Team</span></div>
          <!-- TODO: Write full article content -->
          <span class="mag-card-todo">Article to be written</span>
        </div>
      </article>
      <article class="mag-card">
        <div class="mag-card-img"><span class="mag-card-img-placeholder">Image coming soon</span></div>
        <div class="mag-card-body">
          <div class="mag-card-cat">Operator insights</div>
          <h3 class="mag-card-title">Dynamic pricing in ski resorts: how to maximise RevPAR on a premium chalet</h3>
          <div class="mag-card-meta"><span>7 min</span><span>·</span><span>ALPÉON Team</span></div>
          <!-- TODO: Write full article content -->
          <span class="mag-card-todo">Article to be written</span>
        </div>
      </article>
      <article class="mag-card">
        <div class="mag-card-img"><span class="mag-card-img-placeholder">Image coming soon</span></div>
        <div class="mag-card-body">
          <div class="mag-card-cat">Operator insights</div>
          <h3 class="mag-card-title">Guaranteed rent vs. commission: the questions every property owner should ask</h3>
          <div class="mag-card-meta"><span>6 min</span><span>·</span><span>ALPÉON Team</span></div>
          <!-- TODO: Write full article content -->
          <span class="mag-card-todo">Article to be written</span>
        </div>
      </article>
    </div>

  </div>

  <section class="mag-cta">
    <div class="mag-cta-inner">
      <div style="font-size:.72rem;letter-spacing:.2em;text-transform:uppercase;color:rgba(232,203,160,.7);margin-bottom:1.25rem">Alpine property owner</div>
      <h2>Estimate your <em>rental income</em></h2>
      <p>Calculate what your alpine chalet or apartment can generate with ALPÉON. Free, no commitment, in 2 minutes.</p>
      <a href="/en/estimateur/" class="btn-gold">
        Run the estimate
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
      </a>
    </div>
  </section>

  <!-- EN FOOTER (translated) -->
  {footer_html.replace(
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
    '/loyer-garanti/', '/en/guaranteed-rent/'
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
  ).replace(
    "Propriétaires", "Owners"
  ).replace(
    "ALPÉON Signatures", "ALPÉON Signatures"
  ).replace(
    "Estimateur de revenus", "Revenue estimator"
  ).replace(
    "Loyer garanti", "Guaranteed rent"
  ).replace(
    "À propos", "About"
  ).replace(
    "Mentions légales", "Legal notice"
  ).replace(
    "Politique de confidentialité", "Privacy policy"
  ).replace(
    "Conditions générales", "Terms"
  ).replace(
    "Appelez-nous", "Call us"
  )}

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

# Create directories and write files
os.makedirs(f'{BASE}/magazine', exist_ok=True)
with open(f'{BASE}/magazine/index.html', 'w', encoding='utf-8') as f:
    f.write(FR_HTML)
print('Created: magazine/index.html')

os.makedirs(f'{BASE}/en/magazine', exist_ok=True)
with open(f'{BASE}/en/magazine/index.html', 'w', encoding='utf-8') as f:
    f.write(EN_HTML)
print('Created: en/magazine/index.html')
