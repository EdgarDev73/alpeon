/**
 * GET /api/properties/:id
 * Returns a single Guesty listing, normalised.
 *
 * Cache mémoire Lambda 5 min + stale-if-error 1h côté Vercel CDN.
 * Même résilience que /api/properties : un token expiré ne casse pas la page.
 */
const { getListing, normalizeListing } = require('../../_lib/guesty');

// Cache mémoire par listing (instance Lambda chaude)
const _cache = new Map(); // id → { data, fetchedAt }
const CACHE_TTL = 5 * 60 * 1000; // 5 min

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'GET') return res.status(405).json({ error: 'Method not allowed' });

  const id = req.query.id;
  if (!id) return res.status(400).json({ error: 'Missing id' });

  const now = Date.now();
  const cached = _cache.get(id);

  try {
    // Servir depuis le cache mémoire si frais
    if (cached && now - cached.fetchedAt < CACHE_TTL) {
      res.setHeader('Cache-Control', 's-maxage=300, stale-while-revalidate=60, stale-if-error=3600');
      return res.status(200).json({ property: cached.data });
    }

    const raw = await getListing(id);
    const property = normalizeListing(raw);
    _cache.set(id, { data: property, fetchedAt: now });

    res.setHeader('Cache-Control', 's-maxage=300, stale-while-revalidate=60, stale-if-error=3600');
    return res.status(200).json({ property });

  } catch (err) {
    console.error('[properties/[id]]', err.message);

    // Fallback : servir le cache stale plutôt qu'une 500
    if (cached) {
      console.warn('[properties/[id]] Serving stale cache after Guesty error for', id);
      res.setHeader('Cache-Control', 'no-store');
      return res.status(200).json({ property: cached.data, _stale: true });
    }

    return res.status(500).json({ error: err.message });
  }
};
