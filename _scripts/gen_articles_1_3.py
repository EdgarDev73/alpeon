#!/usr/bin/env python3
"""Generate first 3 magazine articles for ALPÉON."""
import os, textwrap

BASE = "/Users/edgarvernet/claude/alpeon"

# ── Shared blocks ────────────────────────────────────────────────────────────

GTM = """  <!-- Consent Mode v2 — RGPD -->
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    var _ac = localStorage.getItem('alpeon_cookie_consent');
    gtag('consent', 'default', {
      'analytics_storage': _ac === 'granted' ? 'granted' : 'denied',
      'ad_storage': 'denied',
      'wait_for_update': 500
    });
  </script>
  <!-- Google Tag Manager -->
  <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-PXZ2KXWV');</script>
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-XCYNTWQ9HX"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-XCYNTWQ9HX');
  </script>"""

FAVICONS = """  <link rel="icon" type="image/x-icon" href="/assets/logo/favicon.ico">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/logo/favicon-32.png">
  <link rel="icon" type="image/png" sizes="180x180" href="/assets/logo/favicon-180.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/logo/favicon-180.png">"""

FONTS = """  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400;1,500;1,600&display=swap" rel="stylesheet" />"""

NAV_CSS = """  /* @@NAV-START@@ */
  :root { --nav-h: 88px; }
  .site-header {
    position: fixed; top: 0; left: 0; right: 0; z-index: 300;
    height: var(--nav-h); background: transparent;
    border-bottom: 1px solid transparent;
    transition: background .35s ease, border-color .35s ease;
  }
  .site-header.scrolled {
    background: rgba(18,30,20,.97);
    backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
    border-bottom: 1px solid rgba(232,203,160,.1);
  }
  .site-header-inner {
    max-width: 1400px; margin: 0 auto;
    padding: 0 2.5rem; height: var(--nav-h); display: flex; align-items: center;
  }
  .site-logo { display: flex; align-items: center; text-decoration: none; flex-shrink: 0; }
  .site-logo img { height: 64px; width: auto; display: block; }
  .site-nav { display: flex; align-items: center; gap: 2rem; margin-left: auto; }
  .site-nav-link {
    color: rgba(250,254,255,.75); font-size: .85rem; font-weight: 500;
    letter-spacing: .12em; text-transform: uppercase; text-decoration: none;
    position: relative; padding-bottom: 3px; transition: color .2s; white-space: nowrap;
  }
  .site-nav-link::after {
    content: ''; position: absolute; bottom: 0; left: 0; right: 0;
    height: 1.5px; background: #C9A97A;
    transform: scaleX(0); transform-origin: left; transition: transform .25s ease;
  }
  .site-nav-link:hover { color: #fff; }
  .site-nav-link.active { color: #C9A97A; }
  .site-nav-link.active::after, .site-nav-link:hover::after { transform: scaleX(1); }
  .site-header-right { display: flex; align-items: center; gap: 1.25rem; margin-left: 2.5rem; flex-shrink: 0; }
  .site-lang { display: flex; align-items: center; gap: .35rem; font-size: .65rem; letter-spacing: .1em; text-transform: uppercase; }
  .site-lang a { color: rgba(250,254,255,.35); text-decoration: none; transition: color .2s; }
  .site-lang a.active { color: #C9A97A; }
  .site-lang span { color: rgba(250,254,255,.15); font-size: .5rem; }
  .site-burger { display: none; flex-direction: column; justify-content: center; gap: 5px; width: 28px; height: 28px; background: none; border: none; cursor: pointer; padding: 0; }
  .site-burger span { display: block; height: 1.5px; background: rgba(250,254,255,.75); border-radius: 2px; transition: all .25s; }
  .site-burger.open span:nth-child(1) { transform: translateY(6.5px) rotate(45deg); }
  .site-burger.open span:nth-child(2) { opacity: 0; }
  .site-burger.open span:nth-child(3) { transform: translateY(-6.5px) rotate(-45deg); }
  .site-mobile-menu {
    display: none; position: fixed; top: var(--nav-h); left: 0; right: 0; bottom: 0;
    background: rgb(18,30,20);
    flex-direction: column; padding: 2rem 2rem 3rem; z-index: 9999;
    opacity: 0; pointer-events: none; transition: opacity .25s;
  }
  .site-mobile-menu.open { opacity: 1; pointer-events: all; }
  .site-mobile-link {
    color: rgba(250,254,255,.6); font-size: 1.1rem; font-weight: 300;
    letter-spacing: .12em; text-transform: uppercase; text-decoration: none;
    padding: 1rem 0; border-bottom: 1px solid rgba(250,254,255,.06); transition: color .2s;
    font-family: var(--font-sans);
  }
  .site-mobile-link:hover, .site-mobile-link.active { color: #C9A97A; }
  .site-mobile-lang { display: flex; gap: .5rem; align-items: center; font-size: .7rem; letter-spacing: .1em; text-transform: uppercase; color: rgba(250,254,255,.3); margin-top: 1.5rem; }
  .site-mobile-lang a { color: rgba(250,254,255,.35); text-decoration: none; transition: color .2s; }
  .site-mobile-lang a.active { color: #C9A97A; }
  @media (max-width: 900px) {
    .site-nav, .site-lang { display: none; }
    .site-burger { display: flex; }
    .site-mobile-menu { display: flex; }
    .site-header-inner { padding: 0 1.25rem; }
    .site-logo img { height: 48px; }
    .site-header-right { margin-left: auto; }
  }
  .hdr-phone-wrap { position: relative; }
  .hdr-phone-btn { display: flex; align-items: center; background: none; border: none; padding: .35rem; color: rgba(232,203,160,.55); cursor: pointer; transition: color .2s; flex-shrink: 0; }
  .hdr-phone-btn:hover { color: var(--gold,#E8CBA0); }
  .hdr-phone-btn svg { width: 17px; height: 17px; stroke: currentColor; fill: none; stroke-width: 1.75; flex-shrink: 0; }
  .hdr-phone-dropdown { display: none; position: absolute; top: 100%; right: 0; padding-top: 6px; background: #1a2a1e; border: 1px solid rgba(232,203,160,.15); border-radius: 8px; min-width: 260px; overflow: hidden; box-shadow: 0 16px 48px rgba(0,0,0,.45); z-index: 900; }
  .hdr-phone-wrap.open .hdr-phone-dropdown { display: block; }
  .hdr-phone-item { display: flex; align-items: center; gap: 12px; padding: 13px 18px; color: rgba(250,254,255,.75); font-size: .82rem; transition: background .2s; text-decoration: none; white-space: nowrap; }
  .hdr-phone-item:hover { background: rgba(232,203,160,.08); color: var(--gold,#E8CBA0); }
  .hdr-phone-item + .hdr-phone-item { border-top: 1px solid rgba(250,254,255,.07); }
  .hdr-phone-item svg { width: 16px; height: 16px; flex-shrink: 0; }
  .hdr-phone-item .hdr-phone-icon-tel { stroke: currentColor; fill: none; stroke-width: 2; }
  .hdr-lang-wrap { position: relative; display: none; }
  @media (max-width: 900px) { .hdr-lang-wrap { display: flex; align-items: center; } }
  .hdr-lang-btn { display: flex; align-items: center; background: none; border: none; padding: .35rem; color: rgba(232,203,160,.55); cursor: pointer; transition: color .2s; flex-shrink: 0; }
  .hdr-lang-btn:hover { color: var(--gold,#E8CBA0); }
  .hdr-lang-btn svg { width: 17px; height: 17px; stroke: currentColor; fill: none; stroke-width: 1.75; flex-shrink: 0; }
  .hdr-lang-dropdown { display: none; position: absolute; top: calc(100% + 6px); right: 0; background: #1a2a1e; border: 1px solid rgba(232,203,160,.15); border-radius: 8px; min-width: 110px; overflow: hidden; box-shadow: 0 16px 48px rgba(0,0,0,.45); z-index: 900; }
  .hdr-lang-wrap.open .hdr-lang-dropdown { display: block; }
  .hdr-lang-item { display: flex; align-items: center; gap: 8px; padding: 11px 16px; color: rgba(250,254,255,.75); font-size: .78rem; letter-spacing: .08em; text-transform: uppercase; transition: background .2s; text-decoration: none; white-space: nowrap; }
  .hdr-lang-item:hover { background: rgba(232,203,160,.08); color: var(--gold,#E8CBA0); }
  .hdr-lang-item.active { color: #C9A97A; }
  .hdr-lang-item + .hdr-lang-item { border-top: 1px solid rgba(250,254,255,.07); }
  /* @@NAV-END@@ */"""

ARTICLE_CSS = """
  /* ── Breadcrumb ── */
  .breadcrumb-list { display: flex; align-items: center; gap: .4rem; list-style: none; flex-wrap: wrap; }
  .breadcrumb-list li { display: flex; align-items: center; gap: .4rem; }
  .breadcrumb-list li::before { content: '›'; color: rgba(250,254,255,.25); font-size: .8rem; }
  .breadcrumb-list li:first-child::before { display: none; }
  .breadcrumb-list a { color: rgba(250,254,255,.35); font-size: .72rem; letter-spacing: .06em; text-transform: uppercase; transition: color .2s; }
  .breadcrumb-list a:hover { color: var(--gold); }
  .breadcrumb-list span { color: rgba(250,254,255,.55); font-size: .72rem; letter-spacing: .06em; text-transform: uppercase; }

  /* ── Article hero ── */
  .art-hero { padding: 32px var(--pad) 0; max-width: 860px; margin: 0 auto; }
  .art-cat-badge { display: inline-block; font-size: .62rem; font-weight: 600; letter-spacing: .18em; text-transform: uppercase; color: var(--gold); border: 1px solid rgba(232,203,160,.3); border-radius: 3px; padding: .25rem .65rem; margin-bottom: 1.25rem; }
  .art-hero h1 { font-family: var(--font-serif); font-size: clamp(1.8rem, 4vw, 3rem); font-weight: 400; line-height: 1.18; color: #fff; margin-bottom: 1.25rem; }
  .art-hero h1 em { font-style: italic; color: var(--gold); }
  .art-meta { display: flex; align-items: center; gap: .75rem; flex-wrap: wrap; font-size: .72rem; color: rgba(250,254,255,.35); letter-spacing: .04em; margin-bottom: 2rem; }
  .art-meta span { display: flex; align-items: center; gap: .3rem; }
  .art-lead { font-size: 1.05rem; font-weight: 300; color: rgba(250,254,255,.65); line-height: 1.85; max-width: 720px; border-left: 2px solid rgba(232,203,160,.35); padding-left: 1.25rem; margin-bottom: 3rem; }

  /* ── Article layout ── */
  .art-layout { display: grid; grid-template-columns: 220px 1fr; gap: 64px; max-width: 1100px; margin: 0 auto; padding: 0 var(--pad) 80px; align-items: start; }
  @media (max-width: 900px) { .art-layout { grid-template-columns: 1fr; gap: 0; } }

  /* ── TOC ── */
  .art-toc { position: sticky; top: calc(var(--nav-h) + 2rem); }
  .art-toc-title { font-size: .62rem; font-weight: 600; letter-spacing: .2em; text-transform: uppercase; color: rgba(250,254,255,.25); margin-bottom: 1rem; }
  .art-toc-list { list-style: none; display: flex; flex-direction: column; gap: .5rem; }
  .art-toc-list a { font-size: .78rem; font-weight: 300; color: rgba(250,254,255,.38); text-decoration: none; line-height: 1.5; transition: color .2s; display: block; padding: .2rem 0; border-left: 1.5px solid transparent; padding-left: .75rem; }
  .art-toc-list a:hover, .art-toc-list a.active { color: var(--gold); border-left-color: var(--gold); }
  @media (max-width: 900px) { .art-toc { display: none; } }

  /* ── Article body ── */
  .art-body { min-width: 0; }
  .art-body h2 { font-family: var(--font-serif); font-size: clamp(1.3rem, 2.5vw, 1.75rem); font-weight: 400; color: #fff; margin: 2.75rem 0 1rem; padding-top: .25rem; line-height: 1.3; }
  .art-body h2:first-child { margin-top: 0; }
  .art-body h3 { font-size: 1rem; font-weight: 500; color: rgba(250,254,255,.85); margin: 1.75rem 0 .6rem; }
  .art-body p { font-size: .9rem; color: rgba(250,254,255,.6); line-height: 1.85; margin-bottom: 1rem; }
  .art-body p strong { color: rgba(250,254,255,.85); font-weight: 500; }
  .art-body ul { margin: .5rem 0 1rem 1.25rem; display: flex; flex-direction: column; gap: .5rem; }
  .art-body ul li { font-size: .9rem; color: rgba(250,254,255,.6); line-height: 1.75; list-style: disc; }
  .art-body ul li strong { color: rgba(250,254,255,.85); font-weight: 500; }
  .art-body hr { border: none; border-top: 1px solid rgba(250,254,255,.07); margin: 2.5rem 0; }

  /* ── Key box ── */
  .key-box { background: rgba(232,203,160,.07); border: 1px solid rgba(232,203,160,.2); border-radius: 10px; padding: 1.5rem 1.75rem; margin: 2rem 0; }
  .key-box-title { font-size: .62rem; font-weight: 600; letter-spacing: .18em; text-transform: uppercase; color: var(--gold); margin-bottom: 1rem; }
  .key-stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.25rem; }
  @media (max-width: 600px) { .key-stats { grid-template-columns: 1fr; } }
  .key-stat-num { font-family: var(--font-serif); font-size: 2rem; font-weight: 400; color: var(--gold); line-height: 1; margin-bottom: .25rem; }
  .key-stat-label { font-size: .75rem; color: rgba(250,254,255,.45); line-height: 1.5; }

  /* ── Tip box ── */
  .tip-box { background: rgba(44,61,48,.35); border-left: 3px solid rgba(232,203,160,.5); border-radius: 0 8px 8px 0; padding: 1.25rem 1.5rem; margin: 2rem 0; }
  .tip-box-label { font-size: .62rem; font-weight: 600; letter-spacing: .18em; text-transform: uppercase; color: var(--gold); margin-bottom: .5rem; }
  .tip-box p { margin: 0; font-size: .85rem; }

  /* ── Comparison table ── */
  .cmp-table { width: 100%; border-collapse: collapse; margin: 1.5rem 0 2rem; font-size: .83rem; }
  .cmp-table th { padding: .75rem 1rem; text-align: left; font-size: .62rem; font-weight: 600; letter-spacing: .14em; text-transform: uppercase; color: rgba(250,254,255,.3); border-bottom: 1px solid rgba(250,254,255,.08); }
  .cmp-table th:nth-child(2) { color: var(--gold); }
  .cmp-table td { padding: .8rem 1rem; border-bottom: 1px solid rgba(250,254,255,.06); color: rgba(250,254,255,.55); vertical-align: top; line-height: 1.5; }
  .cmp-table td:first-child { color: rgba(250,254,255,.35); font-size: .75rem; text-transform: uppercase; letter-spacing: .06em; }
  .cmp-table td:nth-child(2) { color: rgba(250,254,255,.8); }
  .cmp-check { color: #86efac; }
  .cmp-cross { color: rgba(250,100,100,.65); }
  @media (max-width: 600px) { .cmp-table th, .cmp-table td { padding: .6rem .6rem; } }

  /* ── Related articles ── */
  .art-related { max-width: 1100px; margin: 0 auto; padding: 0 var(--pad) 80px; }
  .art-related-title { font-size: .62rem; font-weight: 600; letter-spacing: .2em; text-transform: uppercase; color: rgba(250,254,255,.25); margin-bottom: 1.5rem; }
  .art-related-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }
  @media (max-width: 700px) { .art-related-grid { grid-template-columns: 1fr; } }
  .art-related-card { display: block; background: rgba(250,254,255,.03); border: 1px solid rgba(250,254,255,.06); border-radius: 8px; padding: 1.25rem; text-decoration: none; transition: border-color .2s, background .2s; }
  .art-related-card:hover { border-color: rgba(232,203,160,.25); background: rgba(232,203,160,.04); }
  .art-related-cat { font-size: .6rem; font-weight: 600; letter-spacing: .15em; text-transform: uppercase; color: var(--gold); opacity: .75; margin-bottom: .5rem; }
  .art-related-title-text { font-size: .85rem; font-weight: 400; color: rgba(250,254,255,.7); line-height: 1.5; }
  .art-related-meta { font-size: .7rem; color: rgba(250,254,255,.25); margin-top: .6rem; }

  /* ── CTA ── */
  .art-cta { background: var(--green); padding: 80px var(--pad); text-align: center; }
  .art-cta-inner { max-width: 620px; margin: 0 auto; }
  .art-cta-eyebrow { font-size: .72rem; letter-spacing: .2em; text-transform: uppercase; color: rgba(232,203,160,.7); margin-bottom: 1.25rem; }
  .art-cta h2 { font-family: var(--font-serif); font-size: clamp(1.6rem, 3.5vw, 2.4rem); color: #fff; margin-bottom: 1rem; }
  .art-cta h2 em { font-style: italic; color: var(--gold); }
  .art-cta p { color: rgba(250,254,255,.55); margin-bottom: 2rem; font-size: .9rem; }
  .btn-gold { display: inline-flex; align-items: center; gap: .5rem; background: var(--gold); color: var(--ink); padding: .9rem 2rem; border-radius: 4px; font-size: .8rem; font-weight: 600; letter-spacing: .12em; text-transform: uppercase; transition: background .2s; text-decoration: none; }
  .btn-gold:hover { background: var(--gold-d); }"""

FOOTER_CSS = """
  /* ── Footer ── */
  .footer-owner-cta { border-top: none; padding: .85rem 0; }
  .footer-owner-flex { display: flex; align-items: center; justify-content: center; gap: .7rem; flex-wrap: wrap; }
  .footer-owner-sep { color: rgba(250,254,255,.18); font-size: .7rem; line-height: 1; }
  .footer-owner-text { color: rgba(250,254,255,.3); font-size: .72rem; font-family: var(--font-sans); font-weight: 300; letter-spacing: .03em; }
  .footer-owner-btn { display: inline-flex; align-items: center; gap: .3rem; color: rgba(232,203,160,.5); font-size: .72rem; font-family: var(--font-sans); font-weight: 400; letter-spacing: .03em; text-decoration: none; transition: color .2s; white-space: nowrap; }
  .footer-owner-btn:hover { color: #E8CBA0; }
  footer { background: #0d1410; padding: 0; border-top: 1px solid rgba(232,203,160,.12); }
  footer > .container { padding-top: clamp(48px,6vw,72px); }
  .footer-grid { display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 48px; padding-bottom: 48px; border-bottom: 1px solid rgba(250,254,255,.07); }
  .footer-brand-logo { margin-bottom: 14px; }
  .footer-brand-claim { font-size: .58rem; font-weight: 600; letter-spacing: .22em; text-transform: uppercase; color: var(--gold,#E8CBA0); margin-bottom: 16px; opacity: .85; }
  .footer-brand-text { font-size: .81rem; font-weight: 300; color: rgba(250,254,255,.32); line-height: 1.8; max-width: 270px; }
  .footer-col-title { font-size: .58rem; font-weight: 600; letter-spacing: .2em; text-transform: uppercase; color: rgba(250,254,255,.22); margin-bottom: 18px; }
  .footer-links { list-style: none; display: flex; flex-direction: column; gap: 11px; }
  .footer-links a { font-size: .83rem; font-weight: 300; color: rgba(250,254,255,.48); transition: color .2s; text-decoration: none; }
  .footer-links a:hover { color: var(--gold,#E8CBA0); }
  .footer-lower { display: grid; grid-template-columns: 1fr 2fr; gap: 48px; padding: 40px 0 48px; border-bottom: 1px solid rgba(250,254,255,.07); }
  .footer-socials { display: flex; gap: 14px; align-items: center; margin-top: 4px; }
  .footer-social-link { display: flex; align-items: center; justify-content: center; width: 36px; height: 36px; border-radius: 50%; border: 1px solid rgba(250,254,255,.15); color: rgba(250,254,255,.48); transition: all .2s; }
  .footer-social-link:hover { border-color: var(--gold,#E8CBA0); color: var(--gold,#E8CBA0); background: rgba(232,203,160,.07); }
  .footer-social-link svg { width: 16px; height: 16px; fill: currentColor; }
  .nl-form { display: flex; gap: 8px; margin-top: 4px; }
  .nl-input { flex: 1; border: 1px solid rgba(250,254,255,.12); border-radius: 4px; background: rgba(250,254,255,.05); color: #fff; padding: .55rem .85rem; font-size: .8rem; font-family: inherit; outline: none; transition: border-color .2s; }
  .nl-input::placeholder { color: rgba(250,254,255,.25); }
  .nl-input:focus { border-color: rgba(232,203,160,.45); }
  .nl-btn { background: var(--gold,#E8CBA0); color: #1a2a1e; border: none; border-radius: 4px; padding: .55rem 1.1rem; font-size: .72rem; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; cursor: pointer; white-space: nowrap; transition: opacity .2s; font-family: inherit; }
  .nl-btn:hover { opacity: .85; }
  .nl-msg { font-size: .73rem; margin-top: .5rem; min-height: 1em; }
  .nl-msg.ok { color: #86efac; } .nl-msg.err { color: #fca5a5; }
  .footer-bottom { padding: 24px 0; display: flex; justify-content: space-between; align-items: center; gap: 12px; }
  .footer-bottom span { font-size: .68rem; color: rgba(250,254,255,.18); }
  @media(max-width:1024px){ .footer-grid{ grid-template-columns:1fr 1fr; gap:36px; } .footer-lower{ grid-template-columns:1fr; } }
  @media(max-width:600px){ .footer-grid{ grid-template-columns:1fr; } .footer-bottom{ flex-direction:column; text-align:center; } }"""


def header_html(fr_url, en_url):
    return f"""  <header class="site-header" id="site-header">
  <div class="site-header-inner">
    <a href="/accueil/" class="site-logo">
      <img src="/assets/logo/logo-main-gold.svg" alt="ALPÉON">
    </a>
    <nav class="site-nav">
      <a href="/accueil/" class="site-nav-link">Accueil</a>
      <a href="/proprietaires/" class="site-nav-link">Propriétaires</a>
      <a href="/estimateur/" class="site-nav-link">Estimateur</a>
      <a href="/reserver/" class="site-nav-link">Réserver</a>
      <a href="/destinations/" class="site-nav-link">Destinations</a>
      <a href="/about/" class="site-nav-link">À propos</a>
    </nav>
    <div class="site-header-right">
      <div class="hdr-phone-wrap">
        <button class="hdr-phone-btn" onclick="this.closest('.hdr-phone-wrap').classList.toggle('open')">
          <svg viewBox="0 0 24 24"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.86 13a19.79 19.79 0 01-3.07-8.67A2 2 0 012.77 2h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L6.91 9.91a16 16 0 006.18 6.18l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z"/></svg>
        </button>
        <div class="hdr-phone-dropdown">
          <a href="tel:+33970703991" class="hdr-phone-item">
            <svg class="hdr-phone-icon-tel" viewBox="0 0 24 24"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.86 13a19.79 19.79 0 01-3.07-8.67A2 2 0 012.77 2h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L6.91 9.91a16 16 0 006.18 6.18l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z"/></svg>
            Appelez-nous
          </a>
          <a href="https://wa.me/33698967306?text=I+would+like+to+manage+my+property+by+Alp%C3%A9on" class="hdr-phone-item">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
            WhatsApp
          </a>
        </div>
      </div>
      <div class="hdr-lang-wrap" id="hdr-lang-wrap">
        <button class="hdr-lang-btn" onclick="toggleLangDropdown()" aria-label="Changer de langue">
          <svg viewBox="0 0 24 24" stroke="currentColor" fill="none" stroke-width="1.75"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
        </button>
        <div class="hdr-lang-dropdown" id="hdr-lang-dropdown"></div>
      </div>
      <div class="site-lang">
        <a href="{fr_url}" class="active">FR</a>
        <span>|</span>
        <a href="{en_url}">EN</a>
      </div>
      <button class="site-burger" id="site-burger" aria-label="Menu" onclick="toggleMobileMenu()">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
</header>
<nav class="site-mobile-menu" id="mobile-menu">
  <a href="/accueil/" class="site-mobile-link">Accueil</a>
  <a href="/proprietaires/" class="site-mobile-link">Propriétaires</a>
  <a href="/estimateur/" class="site-mobile-link">Estimateur</a>
  <a href="/reserver/" class="site-mobile-link">Réserver</a>
  <a href="/destinations/" class="site-mobile-link">Destinations</a>
  <a href="/about/" class="site-mobile-link">À propos</a>
  <div class="site-mobile-lang">
    <a href="{fr_url}" class="active">FR</a>
    <span>|</span>
    <a href="{en_url}">EN</a>
  </div>
</nav>"""


FOOTER_HTML = """  <footer id="contact">
<div class="footer-owner-cta">
  <div class="container footer-owner-flex">
    <span class="footer-owner-text">Propriétaire d'un bien alpin ?</span>
    <span class="footer-owner-sep">·</span>
    <a href="/estimateur/" class="footer-owner-btn">
      Estimez vos revenus
      <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
    </a>
  </div>
</div>
  <div class="container">
    <div class="footer-grid">
      <div>
        <div class="footer-brand-logo">
          <img src="/assets/logo/logo-main-gold.svg" alt="ALPÉON" height="110" style="height:110px;width:auto;display:block">
        </div>
        <div class="footer-brand-claim">Alpine Property Management</div>
        <p class="footer-brand-text">Opérateur premium de gestion locative courte durée dans les Alpes françaises. Discrétion, excellence et transparence.</p>
      </div>
      <div>
        <div class="footer-col-title">Destinations</div>
        <ul class="footer-links">
          <li><a href="/destinations/courchevel/">Courchevel</a></li>
          <li><a href="/destinations/megeve/">Megève</a></li>
          <li><a href="/destinations/val-d-isere/">Val d'Isère</a></li>
          <li><a href="/destinations/val-thorens/">Val Thorens</a></li>
          <li><a href="/destinations/meribel/">Méribel</a></li>
          <li><a href="/destinations/tignes/">Tignes</a></li>
        </ul>
      </div>
      <div>
        <div class="footer-col-title">Services</div>
        <ul class="footer-links">
          <li><a href="/proprietaires/">Propriétaires</a></li>
          <li><a href="/estimateur/">Estimateur de revenus</a></li>
          <li><a href="/loyer-garanti/">Loyer garanti</a></li>
          <li><a href="/magazine/">Magazine</a></li>
          <li><a href="/about/">À propos</a></li>
          <li><a href="/faq/">FAQ</a></li>
        </ul>
      </div>
      <div>
        <div class="footer-col-title">Contact</div>
        <ul class="footer-links">
          <li><a href="tel:+33970703991">Appelez-nous</a></li>
          <li><a href="/contact/">Envoyez-nous un email</a></li>
          <li><a href="https://wa.me/33698967306?text=I+would+like+to+manage+my+property+by+Alp%C3%A9on">WhatsApp</a></li>
        </ul>
        <div style="margin-top:20px">
          <div class="footer-col-title">Légal</div>
          <ul class="footer-links">
            <li><a href="/mentions-legales/">Mentions légales</a></li>
            <li><a href="/politique-confidentialite/">Politique de confidentialité</a></li>
            <li><a href="/cgv/">Conditions générales</a></li>
          </ul>
        </div>
      </div>
    </div>
    <div class="footer-lower">
      <div>
        <div class="footer-col-title">Réseaux sociaux</div>
        <div class="footer-socials">
          <a href="https://www.instagram.com/alpeon.alps?igsh=OWxnZjdsaXd2aHg3" target="_blank" rel="noopener" class="footer-social-link" aria-label="Instagram">
            <svg viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
          </a>
          <a href="https://www.linkedin.com/company/jupiter-residences1/?viewAsMember=true" target="_blank" rel="noopener" class="footer-social-link" aria-label="LinkedIn">
            <svg viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
          </a>
          <a href="https://wa.me/33698967306?text=I+would+like+to+manage+my+property+by+Alp%C3%A9on" class="footer-social-link footer-social-wa" aria-label="WhatsApp">
            <svg viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
          </a>
        </div>
      </div>
      <div>
        <div class="footer-col-title">Newsletter</div>
        <p style="font-size:.78rem;color:rgba(250,254,255,.35);line-height:1.6;margin-bottom:.75rem">Nouvelles propriétés, offres de saison et actualités alpines.</p>
        <form class="nl-form" onsubmit="submitNewsletter(event)">
          <input class="nl-input" type="email" id="nl-email" placeholder="votre@email.fr" required>
          <button class="nl-btn" type="submit">S'inscrire</button>
        </form>
        <p class="nl-msg" id="nl-msg"></p>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 ALPÉON. Tous droits réservés.</span>
      <span>ALPÉON est une marque de VerSpi Real Estate</span>
      <span>Gestion locative alpine premium · Alpes françaises</span>
    </div>
  </div>
</footer>"""

SCRIPTS = """<script>
(function(){
  var h=document.getElementById('site-header');
  if(!h)return;
  function u(){h.classList.toggle('scrolled',window.scrollY>40);}
  window.addEventListener('scroll',u,{passive:true});
  u();
})();
function toggleMobileMenu(){
  var b=document.getElementById('site-burger');
  var m=document.getElementById('mobile-menu');
  if(!b||!m)return;
  b.classList.toggle('open');
  m.classList.toggle('open');
}
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
  document.getElementById('nl-msg').textContent='Merci ! Vous êtes inscrit.';
  document.getElementById('nl-msg').className='nl-msg ok';
}
// TOC active link on scroll
(function(){
  var tocLinks = document.querySelectorAll('.art-toc-list a');
  if(!tocLinks.length) return;
  var sections = [];
  tocLinks.forEach(function(a){
    var id = a.getAttribute('href').replace('#','');
    var el = document.getElementById(id);
    if(el) sections.push({el:el, a:a});
  });
  function onScroll(){
    var scrollY = window.scrollY + 140;
    var active = sections[0];
    sections.forEach(function(s){ if(s.el.offsetTop <= scrollY) active = s; });
    tocLinks.forEach(function(a){ a.classList.remove('active'); });
    if(active) active.a.classList.add('active');
  }
  window.addEventListener('scroll', onScroll, {passive:true});
  onScroll();
})();
</script>

<style>
  .wa-btn{position:fixed;bottom:1.5rem;right:1.5rem;z-index:400;background:#2C3D30;border:1px solid rgba(232,203,160,.25);border-radius:50px;display:flex;align-items:center;gap:.5rem;padding:.65rem 1.1rem .65rem .75rem;box-shadow:0 4px 24px rgba(0,0,0,.35);transition:transform .2s,box-shadow .2s;cursor:pointer;text-decoration:none}
  .wa-btn:hover{transform:translateY(-2px);box-shadow:0 6px 32px rgba(0,0,0,.45)}
  .wa-btn svg{width:22px;height:22px;flex-shrink:0}
  .wa-btn-label{font-size:.72rem;font-weight:500;letter-spacing:.06em;text-transform:uppercase;color:rgba(250,254,255,.75);white-space:nowrap}
  .ck-bar{position:fixed;bottom:0;left:0;right:0;z-index:9999;background:#fff;border-top:1px solid #e8cba0;box-shadow:0 -4px 32px rgba(0,0,0,.10);padding:1.1rem 1.5rem;display:flex;align-items:center;gap:1.2rem;flex-wrap:wrap;font-family:'Poppins',sans-serif;transform:translateY(0);transition:transform .35s ease}
  .ck-bar.ck-hidden{transform:translateY(110%)}
  .ck-text{flex:1;min-width:200px;font-size:.75rem;color:#4b5563;line-height:1.6}
  .ck-text a{color:#2C3D30;text-decoration:underline}
  .ck-btns{display:flex;gap:.65rem;flex-shrink:0}
  .ck-btn{padding:.5rem 1.2rem;border-radius:5px;font-family:'Poppins',sans-serif;font-size:.72rem;font-weight:600;letter-spacing:.06em;text-transform:uppercase;cursor:pointer;border:1.5px solid #2C3D30;transition:background .2s,color .2s;white-space:nowrap}
  .ck-btn-refuse{background:#fff;color:#2C3D30}
  .ck-btn-refuse:hover{background:#f3f4f6}
  .ck-btn-accept{background:#2C3D30;color:#E8CBA0;border-color:#2C3D30}
  .ck-btn-accept:hover{background:#3d5442}
  @media(max-width:560px){.ck-bar{flex-direction:column;align-items:flex-start;gap:.85rem}.ck-btns{width:100%;justify-content:flex-end}}
</style>
<div class="ck-bar" id="ck-bar">
  <p class="ck-text">Nous utilisons des cookies analytiques pour mesurer l'audience et améliorer votre expérience. <a href="/politique-confidentialite/">En savoir plus</a></p>
  <div class="ck-btns">
    <button class="ck-btn ck-btn-refuse" onclick="ckRefuse()">Refuser</button>
    <button class="ck-btn ck-btn-accept" onclick="ckAccept()">Accepter</button>
  </div>
</div>
<script>
(function(){var bar=document.getElementById('ck-bar');if(!bar)return;var stored=localStorage.getItem('alpeon_cookie_consent');if(stored){bar.classList.add('ck-hidden');return;}setTimeout(function(){bar.style.display='flex';},600);})();
function ckAccept(){localStorage.setItem('alpeon_cookie_consent','granted');if(typeof gtag==='function')gtag('consent','update',{'analytics_storage':'granted'});document.getElementById('ck-bar').classList.add('ck-hidden');}
function ckRefuse(){localStorage.setItem('alpeon_cookie_consent','denied');document.getElementById('ck-bar').classList.add('ck-hidden');}
</script>
<a class="wa-btn" href="https://wa.me/33698967306?text=I+would+like+to+manage+my+property+by+Alp%C3%A9on" aria-label="WhatsApp ALPÉON">
  <svg viewBox="0 0 24 24" fill="#E8CBA0"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
  <span class="wa-btn-label">Besoin d'aide ?</span>
</a>"""


def build_page(title, meta_desc, canonical, fr_url, en_url, cat, read_time,
               date_str, jsonld, toc_items, breadcrumb_label, body_html, related_html):
    toc_html = "\n".join(
        f'      <li><a href="#{item[0]}">{item[1]}</a></li>'
        for item in toc_items
    )
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
{GTM}
  <meta charset="UTF-8" />
{FAVICONS}
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} | ALPÉON Magazine</title>
  <meta name="description" content="{meta_desc}" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="{canonical}" />
  <link rel="alternate" hreflang="fr" href="{canonical}" />
  <link rel="alternate" hreflang="en" href="https://alpeon.fr{en_url}" />
  <link rel="alternate" hreflang="x-default" href="{canonical}" />
  <meta property="og:type" content="article" />
  <meta property="og:title" content="{title} | ALPÉON Magazine" />
  <meta property="og:description" content="{meta_desc}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="https://alpeon.fr/assets/images/hero-accueil.jpg" />
  <script type="application/ld+json">
  {jsonld}
  </script>
{FONTS}
  <style>
  :root {{
    --green: #2C3D30; --green-d: #223028; --gold: #E8CBA0; --gold-d: #D4B48A;
    --ink: #0d1a0f; --white: #FAFEFF; --stone-1: #F5F3EF; --stone-2: #EAE6DF;
    --black: #111111; --mid: #4A5C4E;
    --font-sans: 'Poppins', sans-serif; --font-serif: 'Poppins', sans-serif;
    --nav-h: 88px; --max: 1380px; --pad: clamp(24px, 5vw, 80px);
  }}
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html {{ scroll-behavior: smooth; -webkit-font-smoothing: antialiased; }}
  body {{ font-family: var(--font-sans); font-weight: 300; background: var(--ink); color: rgba(250,254,255,.85); line-height: 1.6; overflow-x: hidden; }}
  img {{ display: block; max-width: 100%; }}
  a {{ text-decoration: none; color: inherit; }}
  ul {{ list-style: none; }}
  .container {{ width: 100%; max-width: var(--max); margin: 0 auto; padding: 0 var(--pad); }}
{NAV_CSS}
{ARTICLE_CSS}
{FOOTER_CSS}
  </style>
</head>
<body>
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-PXZ2KXWV" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>

{header_html(fr_url, en_url)}

  <!-- BREADCRUMB -->
  <div class="container" style="padding-top: calc(var(--nav-h) + 1rem)">
    <nav class="breadcrumb" aria-label="Fil d'Ariane">
      <ol class="breadcrumb-list">
        <li><a href="/accueil/">Accueil</a></li>
        <li><a href="/magazine/">Magazine</a></li>
        <li><span>{breadcrumb_label}</span></li>
      </ol>
    </nav>
  </div>

  <!-- ARTICLE HERO -->
  <div class="container">
    <div class="art-hero">
      <div class="art-cat-badge">{cat}</div>
      <h1>{title}</h1>
      <div class="art-meta">
        <span>
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
          {date_str}
        </span>
        <span>·</span>
        <span>
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
          {read_time} de lecture
        </span>
        <span>·</span>
        <span>Équipe ALPÉON</span>
      </div>
    </div>
  </div>

  <!-- ARTICLE LAYOUT -->
  <div class="art-layout container">
    <!-- TOC sidebar -->
    <aside class="art-toc">
      <div class="art-toc-title">Sommaire</div>
      <ul class="art-toc-list">
{toc_html}
      </ul>
    </aside>

    <!-- Body -->
    <article class="art-body">
{body_html}
    </article>
  </div>

  <!-- RELATED ARTICLES -->
  <div class="container">
    <div class="art-related">
      <div class="art-related-title">Articles connexes</div>
      <div class="art-related-grid">
{related_html}
      </div>
    </div>
  </div>

  <!-- CTA -->
  <section class="art-cta">
    <div class="art-cta-inner">
      <div class="art-cta-eyebrow">Propriétaire d'un bien alpin</div>
      <h2>Estimez vos <em>revenus locatifs</em></h2>
      <p>Calculez ce que votre chalet ou appartement peut générer avec ALPÉON. Gratuit, sans engagement, en 2 minutes.</p>
      <a href="/estimateur/" class="btn-gold">
        Lancer l'estimation
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
      </a>
    </div>
  </section>

{FOOTER_HTML}

{SCRIPTS}
</body>
</html>"""


def related_card(href, cat, title, read_time):
    return f"""        <a href="{href}" class="art-related-card">
          <div class="art-related-cat">{cat}</div>
          <div class="art-related-title-text">{title}</div>
          <div class="art-related-meta">{read_time} de lecture · Équipe ALPÉON</div>
        </a>"""


# ────────────────────────────────────────────────────────────────────────────
# ARTICLE 1 — Investir à Courchevel en 2025
# ────────────────────────────────────────────────────────────────────────────

ART1_JSONLD = """{
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "BreadcrumbList",
        "itemListElement": [
          { "@type": "ListItem", "position": 1, "name": "Accueil", "item": "https://alpeon.fr/accueil/" },
          { "@type": "ListItem", "position": 2, "name": "Magazine", "item": "https://alpeon.fr/magazine/" },
          { "@type": "ListItem", "position": 3, "name": "Investir à Courchevel en 2025", "item": "https://alpeon.fr/magazine/investir-courchevel-2025/" }
        ]
      },
      {
        "@type": "Article",
        "@id": "https://alpeon.fr/magazine/investir-courchevel-2025/",
        "headline": "Investir à Courchevel en 2025 : les prix, les rendements, les pièges à éviter",
        "description": "Analyse complète du marché immobilier de Courchevel en 2025 : prix au m² par village, rendements locatifs attendus et conseils pour éviter les erreurs.",
        "author": { "@type": "Organization", "name": "Équipe ALPÉON" },
        "publisher": { "@type": "Organization", "@id": "https://alpeon.fr/#organization" },
        "datePublished": "2025-05-14",
        "dateModified": "2025-05-14",
        "inLanguage": "fr",
        "url": "https://alpeon.fr/magazine/investir-courchevel-2025/",
        "image": "https://alpeon.fr/assets/images/dest-courchevel.webp",
        "articleSection": "Investir en station",
        "keywords": ["investir courchevel", "prix immobilier courchevel 2025", "rendement locatif courchevel", "gestion locative courchevel"]
      }
    ]
  }"""

ART1_TOC = [
    ("marche-courchevel-2025", "Le marché en 2025"),
    ("prix-m2-courchevel", "Prix au m² par village"),
    ("rendement-locatif", "Rendements locatifs attendus"),
    ("pieges-eviter", "Les pièges à éviter"),
    ("choisir-operateur", "Choisir le bon opérateur"),
]

ART1_BODY = """      <p class="art-lead">Courchevel concentre à elle seule une part significative des transactions immobilières de luxe dans les Alpes françaises. Mais derrière l'image homogène de la station la plus prisée au monde, le marché est en réalité très segmenté — et les écarts de rendement entre un mauvais et un bon investissement peuvent être considérables.</p>

      <h2 id="marche-courchevel-2025">Le marché immobilier de Courchevel en 2025</h2>
      <p>Courchevel n'est pas une station, c'est un territoire. Avec ses quatre villages — Le Praz (1300), Village (1550), Moriond (1650) et les emblématiques 1850 — la station offre une gamme de biens et de profils d'investissement radicalement différents. En 2025, le marché reste soutenu malgré un contexte de taux d'intérêt encore élevés en Europe. La demande internationale — britannique, moyen-orientale, américaine et scandinave — maintient la pression sur les prix, en particulier à Courchevel 1850.</p>
      <p>Le volume de transactions a légèrement reculé de <strong>8 % en 2024</strong> par rapport au pic de 2022, mais les prix au m² se sont stabilisés à des niveaux historiquement élevés. Les biens de qualité situés à moins de 200 mètres des remontées mécaniques affichent des délais de vente inférieurs à 45 jours — un signe de marché liquide et structurellement tendu.</p>

      <h2 id="prix-m2-courchevel">Prix au m² par village</h2>
      <p>Les fourchettes ci-dessous reflètent les transactions du marché secondaire (revente) pour des biens en bon état. Le neuf en VEFA s'échange généralement avec une prime de 15 à 25 % sur ces références.</p>

      <table class="cmp-table">
        <thead>
          <tr>
            <th>Village</th>
            <th>Fourchette au m²</th>
            <th>Bien type (60 m²)</th>
          </tr>
        </thead>
        <tbody>
          <tr><td>Courchevel 1850</td><td>15 000 – 35 000 €</td><td>900 k€ – 2,1 M€</td></tr>
          <tr><td>Courchevel Moriond (1650)</td><td>8 000 – 14 000 €</td><td>480 k€ – 840 k€</td></tr>
          <tr><td>Courchevel Village (1550)</td><td>5 500 – 9 000 €</td><td>330 k€ – 540 k€</td></tr>
          <tr><td>Le Praz (1300)</td><td>4 000 – 6 500 €</td><td>240 k€ – 390 k€</td></tr>
        </tbody>
      </table>

      <div class="key-box">
        <div class="key-box-title">Courchevel en chiffres — saison 2024-2025</div>
        <div class="key-stats">
          <div>
            <div class="key-stat-num">+12 %</div>
            <div class="key-stat-label">Hausse des prix à 1850 sur 3 ans</div>
          </div>
          <div>
            <div class="key-stat-num">22 sem.</div>
            <div class="key-stat-label">Durée de saison locative effective</div>
          </div>
          <div>
            <div class="key-stat-num">91 %</div>
            <div class="key-stat-label">Taux d'occupation sur les semaines hautes (portefeuille ALPÉON)</div>
          </div>
        </div>
      </div>

      <h2 id="rendement-locatif">Rendements locatifs attendus</h2>
      <p>Le rendement brut à Courchevel dépend étroitement du village, du positionnement du bien et de la qualité de son opérateur. Les fourchettes suivantes sont basées sur les performances réelles du portefeuille ALPÉON :</p>

      <h3>Courchevel 1850 — le haut de gamme absolu</h3>
      <p>À 1850, le chiffre d'affaires locatif peut être élevé en valeur absolue, mais le prix d'acquisition plafonne mécaniquement le rendement brut. Un appartement à <strong>2 M€</strong> générant <strong>120 000 € de revenus annuels</strong> affiche un rendement brut de <strong>6 %</strong> — excellent pour ce segment. Mais après charges (5 à 8 % de la valeur du bien par an), le net descend souvent à 3,5–4,5 %. C'est un investissement patrimonial avant tout : la valorisation du bien dans le temps compense la modestie du rendement net.</p>

      <h3>Courchevel Moriond (1650) — le meilleur ratio valeur/rendement</h3>
      <p>C'est le village qui offre le meilleur équilibre en 2025. Les prix d'acquisition restent accessibles (dès <strong>480 000 €</strong> pour un 2 pièces bien placé), la demande locative est solide (clientèle familiale française et britannique), et les RevPAR au m² sont proches de ceux de 1850. Un bien à <strong>750 000 €</strong> peut générer <strong>48 000 – 58 000 €</strong> de revenus bruts annuels, soit un rendement brut de <strong>6,4 – 7,7 %</strong>.</p>

      <h3>Le Praz et Village (1300-1550) — l'entrée de gamme</h3>
      <p>Ces villages séduisent les acheteurs à budget contraint, mais la demande locative y est plus volatile. Le marché de la location courte durée y est moins profond — la clientèle préfère généralement être au pied des pistes ou en altitude. À retenir uniquement pour un usage mixte (personnel + locatif) ou pour un investisseur avec un horizon long terme.</p>

      <div class="tip-box">
        <div class="tip-box-label">À retenir</div>
        <p>Le rendement brut est une chose, le revenu net en est une autre. Commissions de gestion (20-30 %), charges de copropriété, taxe foncière et entretien peuvent absorber 35 à 50 % de vos recettes brutes. Exigez toujours une simulation nette avant de signer.</p>
      </div>

      <h2 id="pieges-eviter">Les pièges à éviter</h2>

      <h3>Les résidences de tourisme avec promesse de rendement</h3>
      <p>De nombreux promoteurs vendent des appartements en station avec une garantie de loyer sur 9 ou 11 ans. Le pitch est séduisant : loyer garanti, gestion déléguée, récupération de TVA. En pratique, ces promesses cachent souvent des loyers surévalués en début de bail (pour justifier le prix de vente), un gestionnaire imposé peu performant, et des conditions de renouvellement très défavorables au propriétaire. Après la fin du bail, le bien se retrouve souvent dans un état dégradé, avec une valorisation en dessous du marché.</p>

      <h3>Sous-estimer les charges de copropriété</h3>
      <p>À Courchevel, les charges de copropriété dans les résidences de standing peuvent atteindre <strong>80 à 150 € par m² et par an</strong>. Pour un appartement de 60 m², comptez entre <strong>4 800 et 9 000 €</strong> de charges annuelles — avant de payer votre opérateur, la taxe foncière ou l'assurance. Ces charges doivent systématiquement figurer dans votre calcul de rendement net.</p>

      <h3>Ignorer la fiscalité dès l'achat</h3>
      <p>Le choix du régime fiscal (LMNP réel vs micro-BIC, SCI à l'IS vs détention en nom propre) doit être anticipé avant même la signature du compromis. Certaines structures sont impossibles à modifier après l'achat sans coût fiscal significatif. Consultez un conseiller spécialisé en immobilier alpin dès le début de votre démarche.</p>

      <h2 id="choisir-operateur">Choisir le bon opérateur de gestion</h2>
      <p>La qualité de votre opérateur de gestion locative est aussi déterminante que l'emplacement du bien. Un chalet bien situé mal géré peut sous-performer de <strong>25 à 40 %</strong> par rapport à son potentiel. À l'inverse, un bien correctement géré par un opérateur premium avec accès à une base de clients fidèles et une tarification dynamique peut surperformer le marché de <strong>15 à 20 %</strong>.</p>
      <p>Les critères à évaluer : présence physique à Courchevel (pas de gestion depuis Paris ou Lyon), transparence sur la tarification, reporting en temps réel, réseau de distribution multi-canaux (Airbnb, Booking, clientèle directe, agences de voyage de luxe) et bilan de RevPAR vérifiable sur les saisons précédentes.</p>
      <p>ALPÉON gère plus de 200 propriétés sur 6 stations des Alpes françaises, dont un portefeuille significatif à Courchevel. Notre formule <a href="/loyer-garanti/" style="color:var(--gold);text-decoration:underline">loyer garanti</a> permet aux propriétaires de percevoir un revenu fixe mensuel, quelle que soit l'occupation — une alternative particulièrement appréciée des investisseurs qui souhaitent sécuriser leur cash-flow.</p>"""

ART1_RELATED = "\n".join([
    related_card("/magazine/val-d-isere-vs-meribel-rendement-locatif/", "Investir en station",
                 "Val d'Isère vs. Méribel : quel marché offre le meilleur rendement locatif ?", "7 min"),
    related_card("/magazine/neuf-vs-ancien-station-ski/", "Investir en station",
                 "Neuf ou ancien en station de ski : ce que les chiffres disent vraiment", "6 min"),
    related_card("/magazine/loyer-garanti-vs-commission/", "Vie d'opérateur",
                 "Loyer garanti vs. commission : les questions que tout propriétaire doit se poser", "6 min"),
])


# ────────────────────────────────────────────────────────────────────────────
# ARTICLE 2 — Val d'Isère vs. Méribel
# ────────────────────────────────────────────────────────────────────────────

ART2_JSONLD = """{
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "BreadcrumbList",
        "itemListElement": [
          { "@type": "ListItem", "position": 1, "name": "Accueil", "item": "https://alpeon.fr/accueil/" },
          { "@type": "ListItem", "position": 2, "name": "Magazine", "item": "https://alpeon.fr/magazine/" },
          { "@type": "ListItem", "position": 3, "name": "Val d'Isère vs. Méribel", "item": "https://alpeon.fr/magazine/val-d-isere-vs-meribel-rendement-locatif/" }
        ]
      },
      {
        "@type": "Article",
        "@id": "https://alpeon.fr/magazine/val-d-isere-vs-meribel-rendement-locatif/",
        "headline": "Val d'Isère vs. Méribel : quel marché offre le meilleur rendement locatif ?",
        "description": "Comparatif objectif entre Val d'Isère et Méribel : prix au m², profil de clientèle, durée de saison, RevPAR et conseils pour choisir selon votre profil d'investisseur.",
        "author": { "@type": "Organization", "name": "Équipe ALPÉON" },
        "publisher": { "@type": "Organization", "@id": "https://alpeon.fr/#organization" },
        "datePublished": "2025-05-14",
        "dateModified": "2025-05-14",
        "inLanguage": "fr",
        "url": "https://alpeon.fr/magazine/val-d-isere-vs-meribel-rendement-locatif/",
        "image": "https://alpeon.fr/assets/images/hero-accueil.jpg",
        "articleSection": "Investir en station",
        "keywords": ["val d'isère investissement", "méribel rendement locatif", "comparatif stations ski investissement"]
      }
    ]
  }"""

ART2_TOC = [
    ("val-d-isere-profil", "Val d'Isère — le profil"),
    ("meribel-profil", "Méribel — le profil"),
    ("comparatif-rendement", "Comparatif rendement"),
    ("quel-profil-investisseur", "Quel profil pour quel investisseur ?"),
    ("facteur-operateur", "Le facteur décisif : l'opérateur"),
]

ART2_BODY = """      <p class="art-lead">Val d'Isère et Méribel figurent toutes deux dans le top 5 des destinations ski les plus prisées d'Europe. Mais elles n'attirent pas le même profil de locataire, n'affichent pas les mêmes prix d'entrée et ne génèrent pas les mêmes rendements. Ce comparatif vous aide à choisir en fonction de votre stratégie d'investissement.</p>

      <h2 id="val-d-isere-profil">Val d'Isère — la station internationale de haute altitude</h2>
      <p>Val d'Isère, c'est l'Espace Killy : 300 km de pistes partagées avec Tignes, une altitude garantissant l'enneigement de début décembre à début mai, et une réputation mondiale ancrée depuis les Jeux Olympiques de 1992. La station attire une clientèle haut de gamme et internationale — Britanniques, Scandinaves, Américains et Moyen-Orientaux représentent plus de <strong>60 % de la fréquentation</strong>.</p>

      <h3>Le marché immobilier</h3>
      <p>Les prix s'établissent entre <strong>8 000 et 25 000 €/m²</strong> selon la proximité des pistes, le standing et l'altitude. Le centre de Val d'Isère (autour de la place centrale et du front de neige) concentre les biens les plus recherchés. Les appartements skis aux pieds en bon état s'arrachent souvent sans même être mis sur le marché, par réseau.</p>
      <p>Le stock disponible reste structurellement limité : la station est enclavée dans une vallée protégée, sans possibilité d'extension significative. Cette rareté soutient les prix à la hausse sur le long terme — les transactions de 2024 confirment une progression de <strong>+8 % sur 12 mois</strong> pour les biens qualitatifs.</p>

      <h3>La demande locative</h3>
      <p>La saison hivernale court de fin novembre à fin avril — soit <strong>22 à 24 semaines</strong>. Les semaines de Noël, Nouvel An, les vacances britanniques de février et les congés pascaux affichent des taux d'occupation proches de 100 % avec des lead times de réservation supérieurs à 6 mois. Le prix moyen à la nuit pour un appartement 4-6 personnes en semaine haute oscille entre <strong>600 et 1 800 €</strong>.</p>

      <h2 id="meribel-profil">Méribel — le cœur des Trois Vallées</h2>
      <p>Méribel occupe une position centrale dans le domaine skiable des Trois Vallées — le plus grand domaine skiable du monde avec 600 km de pistes. Cette accessibilité est son argument principal : depuis Méribel, on skis vers Courchevel, Val Thorens et les Menuires en un seul domaine, sans reprendre de transport.</p>

      <h3>Le marché immobilier</h3>
      <p>Les prix à Méribel se situent entre <strong>7 000 et 18 000 €/m²</strong>, avec des pics au-delà pour les chalets de luxe en pied de piste. Méribel Village et Méribel-Mottaret (plus haute altitude, accès direct aux remontées) sont les secteurs les plus recherchés. La forte proportion de chalets individuels (vs appartements en résidences) donne à Méribel un charme architectural plus authentique — un argument commercial fort à la location.</p>

      <h3>La demande locative</h3>
      <p>La saison effective est légèrement plus courte qu'à Val d'Isère : <strong>18 à 20 semaines</strong>, avec une demande concentrée sur les vacances scolaires françaises et britanniques. La clientèle est majoritairement française haut de gamme (Île-de-France, grands groupes) et britannique — une homogénéité qui se traduit par des réservations early bird importantes, souvent dès le mois de septembre.</p>

      <h2 id="comparatif-rendement">Comparatif rendement locatif</h2>
      <p>Le tableau suivant compare les performances locatives pour un appartement type de <strong>65 m²</strong>, 4 couchages, bien situé (moins de 300 m des remontées), en bon état — géré par un opérateur professionnel :</p>

      <table class="cmp-table">
        <thead>
          <tr>
            <th>Critère</th>
            <th>Val d'Isère</th>
            <th>Méribel</th>
          </tr>
        </thead>
        <tbody>
          <tr><td>Prix d'acquisition</td><td>780 000 – 1 100 000 €</td><td>560 000 – 850 000 €</td></tr>
          <tr><td>Revenus bruts annuels</td><td>55 000 – 72 000 €</td><td>42 000 – 58 000 €</td></tr>
          <tr><td>Durée de saison</td><td>22 – 24 semaines</td><td>18 – 20 semaines</td></tr>
          <tr><td>Rendement brut estimé</td><td>5,5 – 7,0 %</td><td>6,2 – 7,5 %</td></tr>
          <tr><td>Clientèle principale</td><td>Internationale</td><td>FR + britannique</td></tr>
          <tr><td>Liquidité à la revente</td><td>Très élevée</td><td>Élevée</td></tr>
          <tr><td>Prix moyen nuit haute saison</td><td>900 – 1 800 €</td><td>650 – 1 300 €</td></tr>
        </tbody>
      </table>

      <div class="key-box">
        <div class="key-box-title">L'enseignement clé du comparatif</div>
        <div class="key-stats">
          <div>
            <div class="key-stat-num">+15 %</div>
            <div class="key-stat-label">RevPAR supérieur à Val d'Isère en valeur absolue</div>
          </div>
          <div>
            <div class="key-stat-num">+1,0 pt</div>
            <div class="key-stat-label">Rendement brut meilleur à Méribel en pourcentage</div>
          </div>
          <div>
            <div class="key-stat-num">-28 %</div>
            <div class="key-stat-label">Prix d'entrée inférieur à Méribel pour un bien équivalent</div>
          </div>
        </div>
      </div>

      <h2 id="quel-profil-investisseur">Quel profil pour quel investisseur ?</h2>

      <h3>Choisissez Val d'Isère si…</h3>
      <ul>
        <li>Vous recherchez avant tout la <strong>liquidité et la valorisation patrimoniale</strong> à long terme — Val d'Isère est l'une des rares stations dont la demande à l'achat excède structurellement l'offre.</li>
        <li>Vous visez une <strong>clientèle internationale premium</strong> prête à payer le prix fort pour l'altitude et l'enneigement garanti.</li>
        <li>Votre horizon d'investissement est <strong>supérieur à 10 ans</strong> — le rendement net est plus modeste mais l'appréciation du capital compense.</li>
      </ul>

      <h3>Choisissez Méribel si…</h3>
      <ul>
        <li>Vous souhaitez <strong>optimiser le rendement locatif</strong> sur un prix d'acquisition plus raisonnable, avec un TRI potentiellement supérieur à court terme.</li>
        <li>Vous appréciez <strong>l'authenticité architecturale</strong> — les chalets en savoyard et le cadre village de Méribel sont un argument de vente fort à la location.</li>
        <li>Vous ciblez principalement la <strong>clientèle française et britannique</strong>, qui réserve tôt et offre une forte visibilité revenue à l'avance.</li>
      </ul>

      <h2 id="facteur-operateur">Le facteur décisif : la qualité de l'opérateur</h2>
      <p>Dans les deux cas, la différence entre un investissement rentable et un investissement décevant tient en grande partie à la qualité de l'opérateur de gestion. Un opérateur présent physiquement sur la station, avec une base de clients fidèles, une tarification dynamique et une capacité de commercialisation multi-canaux peut améliorer le RevPAR de <strong>20 à 35 %</strong> par rapport à une gestion en direct ou via une agence locale classique.</p>
      <p>ALPÉON opère sur ces deux stations — et sur quatre autres destinations alpines — avec un portefeuille de plus de 200 propriétés. Notre connaissance fine des marchés locaux, de la saisonnalité et des profils de clientèle nous permet d'optimiser la performance de votre bien quelle que soit la station choisie.</p>"""

ART2_RELATED = "\n".join([
    related_card("/magazine/investir-courchevel-2025/", "Investir en station",
                 "Investir à Courchevel en 2025 : les prix, les rendements, les pièges à éviter", "5 min"),
    related_card("/magazine/neuf-vs-ancien-station-ski/", "Investir en station",
                 "Neuf ou ancien en station de ski : ce que les chiffres disent vraiment", "6 min"),
    related_card("/magazine/tarification-dynamique-revpar/", "Vie d'opérateur",
                 "Tarification dynamique : comment maximiser le RevPAR d'un chalet haut de gamme", "7 min"),
])


# ────────────────────────────────────────────────────────────────────────────
# ARTICLE 3 — Neuf vs. ancien en station
# ────────────────────────────────────────────────────────────────────────────

ART3_JSONLD = """{
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "BreadcrumbList",
        "itemListElement": [
          { "@type": "ListItem", "position": 1, "name": "Accueil", "item": "https://alpeon.fr/accueil/" },
          { "@type": "ListItem", "position": 2, "name": "Magazine", "item": "https://alpeon.fr/magazine/" },
          { "@type": "ListItem", "position": 3, "name": "Neuf ou ancien en station", "item": "https://alpeon.fr/magazine/neuf-vs-ancien-station-ski/" }
        ]
      },
      {
        "@type": "Article",
        "@id": "https://alpeon.fr/magazine/neuf-vs-ancien-station-ski/",
        "headline": "Neuf ou ancien en station de ski : ce que les chiffres disent vraiment",
        "description": "Neuf ou ancien : avantages fiscaux, risques, rendements comparés. Guide pour choisir le bon type de bien immobilier en station alpine.",
        "author": { "@type": "Organization", "name": "Équipe ALPÉON" },
        "publisher": { "@type": "Organization", "@id": "https://alpeon.fr/#organization" },
        "datePublished": "2025-05-14",
        "dateModified": "2025-05-14",
        "inLanguage": "fr",
        "url": "https://alpeon.fr/magazine/neuf-vs-ancien-station-ski/",
        "image": "https://alpeon.fr/assets/images/hero-accueil.jpg",
        "articleSection": "Investir en station",
        "keywords": ["neuf ou ancien station ski", "achat appartement station ski", "LMNP neuf station", "investissement immobilier alpin"]
      }
    ]
  }"""

ART3_TOC = [
    ("avantages-neuf", "Les avantages du neuf"),
    ("pieges-neuf", "Les pièges du neuf"),
    ("avantages-ancien", "Les avantages de l'ancien"),
    ("pieges-ancien", "Les pièges de l'ancien"),
    ("comparatif-chiffre", "Comparatif chiffré"),
    ("conclusion-strategie", "Quelle stratégie adopter ?"),
]

ART3_BODY = """      <p class="art-lead">Acheter un appartement neuf en résidence de tourisme ou un chalet ancien à rénover — les deux options ont leurs défenseurs. Mais au-delà des arguments marketing des promoteurs et des intuitions des investisseurs, les chiffres racontent une histoire souvent contre-intuitive.</p>

      <h2 id="avantages-neuf">Les avantages réels du neuf en station</h2>

      <h3>La récupération de TVA</h3>
      <p>C'est l'argument phare des promoteurs. Acheter un bien neuf dans une résidence de tourisme classée permet de récupérer la <strong>TVA à 20 %</strong> sur le prix d'acquisition — à condition de confier la gestion à un exploitant professionnel via un bail commercial d'au minimum 9 ans. Sur un bien à <strong>600 000 € TTC</strong>, la TVA récupérée représente <strong>100 000 €</strong> — ce qui ramène le prix d'acquisition réel à <strong>500 000 €</strong>.</p>
      <p>Attention toutefois : cette TVA devra être remboursée (au prorata temporis) si vous revendez avant 20 ans ou si vous cessez l'activité para-hôtelière. La TVA est un avantage réel, mais conditionnel.</p>

      <h3>Frais de notaire réduits</h3>
      <p>Pour un bien neuf, les droits de mutation (frais de notaire) s'établissent à <strong>2 à 3 %</strong> du prix de vente, contre <strong>7 à 8 %</strong> pour l'ancien. Sur un bien à 500 000 €, l'économie est de <strong>20 000 à 25 000 €</strong> — non négligeable.</p>

      <h3>Garantie décennale et DPE performant</h3>
      <p>Un bien neuf bénéficie de la garantie décennale (10 ans) et de la biennale (2 ans) sur les équipements. Construit selon la norme RE2020, il affiche un DPE A ou B — un avantage croissant alors que la réglementation sur les passoires thermiques se durcit. En pratique, cela signifie des charges de chauffage 30 à 50 % inférieures à celles d'un bien des années 1980-2000.</p>

      <h2 id="pieges-neuf">Les pièges du neuf que les promoteurs ne mentionnent pas</h2>

      <h3>Le sur-prix promoteur</h3>
      <p>Le neuf en station se vend avec une <strong>prime de 20 à 40 %</strong> sur les prix du marché secondaire pour des biens équivalents. Cette prime est en partie justifiée (TVA récupérable, garanties, frais de notaire réduits), mais elle implique une perte de valeur immédiate à la revente si vous n'attendez pas au moins 5-7 ans. En termes de rendement sur le prix de revient réel, l'avantage TVA est souvent absorbé par ce sur-prix.</p>

      <h3>Le gestionnaire imposé</h3>
      <p>Dans une résidence de tourisme, vous n'avez pas le choix de votre gestionnaire : il est imposé par le bail commercial, généralement pour 9 à 11 ans. Certains exploitants sont excellents, mais d'autres sous-performent significativement. Et si l'exploitant fait faillite (ce qui n'est pas rare dans le secteur), le propriétaire se retrouve dans une situation délicate : il doit soit reprendre lui-même la gestion (et risquer de perdre l'avantage TVA), soit trouver rapidement un nouvel exploitant.</p>

      <h3>Les promesses de rendement souvent fictives</h3>
      <p>Les brochures promotionnelles affichent des rendements garantis de <strong>4 à 6 %</strong>. Ces chiffres sont calculés sur le prix HT (hors TVA), non sur le prix TTC que vous payez réellement. Recalculé sur le prix d'achat réel TTC, le rendement tombe souvent à <strong>2,5 à 3,5 %</strong> — soit moins que certains fonds euros. Et après la période de garantie (3-5 ans), les loyers sont souvent renégociés à la baisse.</p>

      <div class="tip-box">
        <div class="tip-box-label">Règle de prudence</div>
        <p>Avant d'acheter un bien neuf en résidence de tourisme, demandez le bilan d'exploitation des 3 dernières saisons de la résidence — et non les projections du promoteur. Comparez le loyer garanti proposé avec les tarifs pratiqués sur les plateformes pour des biens comparables dans la même station.</p>
      </div>

      <h2 id="avantages-ancien">Les avantages de l'ancien en station</h2>

      <h3>Prix d'entrée inférieur et décote à l'achat</h3>
      <p>Un appartement ancien en bon état dans une station prisée s'achète <strong>20 à 35 % moins cher</strong> qu'un programme neuf équivalent. Cette décote initiale améliore mécaniquement le rendement — à condition que les travaux éventuels soient maîtrisés et budgétisés.</p>

      <h3>Liberté totale dans le choix du gestionnaire</h3>
      <p>Sans bail commercial imposé, vous êtes libre de choisir (et de changer) votre opérateur de gestion locative. C'est un avantage décisif : un opérateur de qualité peut améliorer la performance de votre bien de <strong>20 à 35 %</strong> par rapport à un gestionnaire moyen, grâce à une meilleure commercialisation, une tarification dynamique et une clientèle fidèle.</p>

      <h3>Potentiel de valorisation après rénovation</h3>
      <p>Un ancien bien rénové et ameublé avec goût peut rivaliser avec le neuf en termes de prix à la nuit et de taux d'occupation — en particulier dans les stations qui valorisent le cachet (Megève, Méribel, Val d'Isère). La rénovation permet aussi de déduire les travaux en LMNP réel, amplifiant encore l'avantage fiscal.</p>

      <h2 id="pieges-ancien">Les pièges de l'ancien à anticiper</h2>

      <h3>Le DPE et les obligations énergétiques</h3>
      <p>La loi Climat et Résilience interdit la mise en location des logements classés <strong>G dès 2025</strong>, <strong>F dès 2028</strong> et <strong>E dès 2034</strong>. En station, beaucoup de biens des années 1970-1990 ont des DPE médiocres. Avant tout achat, faites réaliser un DPE pré-achat et chiffrez les travaux nécessaires pour atteindre au moins la classe D. Ces coûts (isolation, chauffage, menuiseries) peuvent représenter <strong>20 000 à 80 000 €</strong> selon la surface et l'état.</p>

      <h3>Les copropriétés vieillissantes</h3>
      <p>En station, les copropriétés des années 1970-1985 accumulent souvent des défauts d'entretien. Avant l'achat, consultez les procès-verbaux des 3 dernières assemblées générales et le carnet d'entretien. Des travaux votés mais non encore engagés (ravalement, toiture, ascenseur) peuvent représenter plusieurs dizaines de milliers d'euros de charges supplémentaires pour les copropriétaires.</p>

      <h2 id="comparatif-chiffre">Comparatif chiffré sur 10 ans</h2>
      <p>Simulation pour un appartement de <strong>55 m²</strong>, 4 couchages, bien situé à Méribel-Moriond :</p>

      <table class="cmp-table">
        <thead>
          <tr>
            <th>Critère</th>
            <th>Neuf (résidence tourisme)</th>
            <th>Ancien rénové (LMNP réel)</th>
          </tr>
        </thead>
        <tbody>
          <tr><td>Prix TTC</td><td>720 000 €</td><td>480 000 € (+ 40 k€ travaux)</td></tr>
          <tr><td>Prix de revient net après TVA</td><td>620 000 €</td><td>520 000 €</td></tr>
          <tr><td>Loyer brut annuel</td><td>25 000 € (garanti exploitant)</td><td>44 000 € (gestion ALPÉON)</td></tr>
          <tr><td>Charges totales / an</td><td>6 000 € (incluses bail)</td><td>14 000 € (copro + gestion + fiscal)</td></tr>
          <tr><td>Revenu net / an</td><td>19 000 €</td><td>30 000 €</td></tr>
          <tr><td>Rendement net</td><td>3,1 %</td><td>5,8 %</td></tr>
          <tr><td>Avantage fiscal (amortissement LMNP)</td><td>Limité (bail commercial)</td><td><span class="cmp-check">✓</span> Plein (régime réel)</td></tr>
          <tr><td>Liberté de gestion</td><td><span class="cmp-cross">✗</span> Gestionnaire imposé</td><td><span class="cmp-check">✓</span> Opérateur au choix</td></tr>
        </tbody>
      </table>

      <h2 id="conclusion-strategie">Quelle stratégie adopter ?</h2>
      <p>La combinaison optimale pour un investisseur cherchant à maximiser son rendement net est <strong>l'ancien rénové en LMNP au régime réel, géré par un opérateur premium</strong>. C'est la formule qui offre le meilleur revenu net, la plus grande flexibilité et l'optimisation fiscale la plus complète via l'amortissement du bien et des travaux.</p>
      <p>Le neuf reste pertinent pour les investisseurs qui veulent une solution clé en main sans gestion, qui ont besoin de financer par emprunt (les banques aiment la garantie décennale) et qui ont un horizon patrimonial long (20 ans+). Mais dans ce cas, choisissez l'exploitant avec autant de soin que l'emplacement.</p>
      <p>Dans tous les cas, <strong>l'emplacement prime sur tout le reste</strong>. Un mauvais bien bien placé surperformera toujours un bon bien mal placé. Skis aux pieds, vue dégagée, proximité des commerces et des remontées mécaniques — ces critères ne se déprécient jamais.</p>"""

ART3_RELATED = "\n".join([
    related_card("/magazine/investir-courchevel-2025/", "Investir en station",
                 "Investir à Courchevel en 2025 : les prix, les rendements, les pièges à éviter", "5 min"),
    related_card("/magazine/lmnp-2025-guide-complet/", "Fiscalité LMNP",
                 "LMNP en 2025 : guide complet pour les propriétaires de biens alpins", "10 min"),
    related_card("/magazine/micro-bic-vs-regime-reel/", "Fiscalité LMNP",
                 "Micro-BIC vs. régime réel : quel choix pour un bien de station haut de gamme ?", "6 min"),
])


# ────────────────────────────────────────────────────────────────────────────
# Generate all 3 articles
# ────────────────────────────────────────────────────────────────────────────

articles = [
    {
        "slug": "investir-courchevel-2025",
        "title": "Investir à Courchevel en 2025 : les prix, les rendements, les pièges à éviter",
        "meta": "Analyse complète du marché immobilier de Courchevel en 2025 : prix au m² par village, rendements locatifs attendus et conseils pour éviter les erreurs coûteuses.",
        "canonical": "https://alpeon.fr/magazine/investir-courchevel-2025/",
        "fr_url": "/magazine/investir-courchevel-2025/",
        "en_url": "/en/magazine/investir-courchevel-2025/",
        "cat": "Investir en station",
        "read": "5 min",
        "date": "14 mai 2025",
        "breadcrumb": "Investir à Courchevel",
        "jsonld": ART1_JSONLD,
        "toc": ART1_TOC,
        "body": ART1_BODY,
        "related": ART1_RELATED,
    },
    {
        "slug": "val-d-isere-vs-meribel-rendement-locatif",
        "title": "Val d'Isère vs. Méribel : quel marché offre le meilleur rendement locatif ?",
        "meta": "Comparatif objectif entre Val d'Isère et Méribel : prix au m², profil de clientèle, durée de saison et rendements. Quel marché choisir selon votre profil d'investisseur ?",
        "canonical": "https://alpeon.fr/magazine/val-d-isere-vs-meribel-rendement-locatif/",
        "fr_url": "/magazine/val-d-isere-vs-meribel-rendement-locatif/",
        "en_url": "/en/magazine/val-d-isere-vs-meribel-rendement-locatif/",
        "cat": "Investir en station",
        "read": "7 min",
        "date": "14 mai 2025",
        "breadcrumb": "Val d'Isère vs. Méribel",
        "jsonld": ART2_JSONLD,
        "toc": ART2_TOC,
        "body": ART2_BODY,
        "related": ART2_RELATED,
    },
    {
        "slug": "neuf-vs-ancien-station-ski",
        "title": "Neuf ou ancien en station de ski : ce que les chiffres disent vraiment",
        "meta": "Neuf ou ancien en station alpine : avantages fiscaux du neuf, liberté de l'ancien, comparatif chiffré sur 10 ans. Ce guide vous aide à faire le bon choix.",
        "canonical": "https://alpeon.fr/magazine/neuf-vs-ancien-station-ski/",
        "fr_url": "/magazine/neuf-vs-ancien-station-ski/",
        "en_url": "/en/magazine/neuf-vs-ancien-station-ski/",
        "cat": "Investir en station",
        "read": "6 min",
        "date": "14 mai 2025",
        "breadcrumb": "Neuf ou ancien en station",
        "jsonld": ART3_JSONLD,
        "toc": ART3_TOC,
        "body": ART3_BODY,
        "related": ART3_RELATED,
    },
]

for a in articles:
    path = os.path.join(BASE, "magazine", a["slug"], "index.html")
    html = build_page(
        title=a["title"],
        meta_desc=a["meta"],
        canonical=a["canonical"],
        fr_url=a["fr_url"],
        en_url=a["en_url"],
        cat=a["cat"],
        read_time=a["read"],
        date_str=a["date"],
        jsonld=a["jsonld"],
        toc_items=a["toc"],
        breadcrumb_label=a["breadcrumb"],
        body_html=a["body"],
        related_html=a["related"],
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✓ Generated {path}")

print("\nDone — 3 articles generated.")
