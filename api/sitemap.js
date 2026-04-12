// api/sitemap.js
const { getListings, normalizeListings } = require('./_lib/guesty');

module.exports = async (req, res) => {
  res.setHeader('Cache-Control', 's-maxage=3600, stale-while-revalidate=86400');
  res.setHeader('Content-Type', 'application/xml; charset=utf-8');

  const BASE = 'https://alpeon.fr';
  const staticPages = [
    { fr: '/accueil/', en: '/en/accueil/', priority: '1.0' },
    { fr: '/reserver/', en: '/en/reserver/', priority: '0.9' },
    { fr: '/destinations/', en: '/en/destinations/', priority: '0.8' },
    { fr: '/proprietaires/', en: '/en/proprietaires/', priority: '0.8' },
    { fr: '/estimateur/', en: '/en/estimateur/', priority: '0.7' },
    { fr: '/about/', en: '/en/about/', priority: '0.6' },
    { fr: '/contact/', en: '/en/contact/', priority: '0.6' },
    { fr: '/faq/', en: '/en/faq/', priority: '0.5' },
  ];

  let propertyUrls = '';
  try {
    const raw = await getListings({ limit: 100 });
    const properties = normalizeListings(raw);
    propertyUrls = properties.map(p => `
  <url>
    <loc>${BASE}/propriete/${p.slug}/${p.id}</loc>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
    <xhtml:link rel="alternate" hreflang="fr" href="${BASE}/propriete/${p.slug}/${p.id}"/>
    <xhtml:link rel="alternate" hreflang="en" href="${BASE}/en/propriete/${p.slug}/${p.id}"/>
  </url>
  <url>
    <loc>${BASE}/en/propriete/${p.slug}/${p.id}</loc>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>`).join('');
  } catch(e) {
    console.error('[sitemap] Could not fetch properties:', e.message);
  }

  const staticUrls = staticPages.map(p => `
  <url>
    <loc>${BASE}${p.fr}</loc>
    <changefreq>weekly</changefreq>
    <priority>${p.priority}</priority>
    <xhtml:link rel="alternate" hreflang="fr" href="${BASE}${p.fr}"/>
    <xhtml:link rel="alternate" hreflang="en" href="${BASE}${p.en}"/>
  </url>
  <url>
    <loc>${BASE}${p.en}</loc>
    <changefreq>weekly</changefreq>
    <priority>${p.priority}</priority>
  </url>`).join('');

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
${staticUrls}
${propertyUrls}
</urlset>`;

  res.status(200).send(xml);
};
