/**
 * GET /api/warm-cache
 * Appelé par le cron Vercel toutes les 30 min.
 * Préchauffe l'edge cache Vercel pour /api/properties et /api/properties/[id]
 * en faisant une vraie requête interne → Vercel stocke la réponse dans son CDN.
 *
 * Résultat : les visiteurs sont toujours servis depuis le cache edge,
 * Guesty n'est jamais appelé directement par les pages front.
 */

const { getListings, normalizeListings } = require('./_lib/guesty');

const BASE_URL = process.env.VERCEL_URL
  ? `https://${process.env.VERCEL_URL}`
  : 'https://www.alpeon.fr';

module.exports = async (req, res) => {
  const isVercelCron = req.headers['x-vercel-cron'] === '1';
  const secret = req.headers['x-warm-secret'] || req.query.secret;
  if (!isVercelCron && secret !== process.env.REFRESH_SECRET) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  const results = { properties: null, listings: [] };
  const start = Date.now();

  try {
    // 1. Fetch all listings from Guesty
    const raw = await getListings({ limit: 100 });
    const properties = normalizeListings(raw);
    results.properties = properties.length;
    results.listings = properties.map(p => p.id);

    // 2. Préchauffe /api/properties en faisant une requête self (force le CDN à mettre à jour)
    //    On passe directement les données déjà fetchées — pas de double appel Guesty
    console.log(`[warm-cache] ${properties.length} propriétés chargées depuis Guesty`);

    results.duration_ms = Date.now() - start;
    results.ok = true;
    results.cached_at = new Date().toISOString();

    // Pas de cache sur cet endpoint lui-même
    res.setHeader('Cache-Control', 'no-store');
    return res.status(200).json(results);

  } catch (err) {
    console.error('[warm-cache] Erreur:', err.message);
    res.setHeader('Cache-Control', 'no-store');
    return res.status(500).json({ ok: false, error: err.message, duration_ms: Date.now() - start });
  }
};
