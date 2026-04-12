/**
 * GET /api/properties
 * Returns live Guesty Booking Engine listings, normalised for ALPÉON UI.
 *
 * Architecture cache multi-niveaux :
 * 1. Cache mémoire Lambda (instance chaude) — TTL 30 min
 * 2. Vercel Edge CDN — s-maxage=1800, stale-while-revalidate=3600, stale-if-error=7j
 * 3. Cron /api/warm-cache toutes les 30 min préchauffe le CDN
 * → Guesty n'est appelé que ~48x/jour, jamais par les visiteurs directement
 */

const { getListings, normalizeListings } = require('./_lib/guesty');

// Cache mémoire pour les instances Lambda chaudes
let _cache = { properties: null, fetchedAt: 0 };
const CACHE_TTL = 30 * 60 * 1000; // 30 min

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'GET') return res.status(405).json({ error: 'Method not allowed' });

  const { city, type, guests, limit = '100', bust } = req.query;
  const bustCache = bust === '1'; // ?bust=1 pour forcer le refresh (cron warm-cache)

  try {
    // 1. Mémoire Lambda : réutiliser si frais et pas de bust
    const now = Date.now();
    if (!bustCache && _cache.properties && now - _cache.fetchedAt < CACHE_TTL) {
      console.log('[properties] Served from Lambda memory cache');
    } else {
      // 2. Fetch depuis Guesty (appel réseau)
      const raw  = await getListings({ limit: parseInt(limit) });
      _cache.properties = normalizeListings(raw);
      _cache.fetchedAt  = now;
      console.log(`[properties] Fetched ${_cache.properties.length} listings from Guesty`);

      // Write fallback (best-effort, non-blocking — silently fails on Vercel read-only FS)
      try {
        const fs = require('fs');
        const path = require('path');
        fs.writeFileSync(
          path.join(__dirname, '../assets/data/properties-fallback.json'),
          JSON.stringify(_cache.properties)
        );
      } catch(e) { /* ignore */ }
    }

    let properties = _cache.properties;

    // Filtres optionnels (server-side)
    if (city && city !== 'all') {
      const norm = s => s.toLowerCase().replace(/['\s]/g, '').replace(/[éè]/g, 'e');
      properties = properties.filter(p => norm(p.city) === norm(city));
    }
    if (type && type !== 'all') {
      properties = properties.filter(p => p.propertyType === type.toLowerCase());
    }
    if (guests && guests !== 'all') {
      const n = parseInt(guests);
      properties = properties.filter(p => guests === '8+' ? p.guests >= 8 : p.guests >= n);
    }

    // Vercel Edge CDN : cache 30 min, stale-while-revalidate 1h, stale-if-error 7 jours
    res.setHeader('Cache-Control', 's-maxage=1800, stale-while-revalidate=3600, stale-if-error=604800');
    return res.status(200).json({ properties, total: properties.length });

  } catch (err) {
    console.error('[properties] Guesty error:', err.message);

    // Servir le cache mémoire stale si disponible plutôt qu'une erreur vide
    if (_cache.properties) {
      console.warn('[properties] Serving stale memory cache after Guesty error');
      res.setHeader('Cache-Control', 'no-store');
      return res.status(200).json({ properties: _cache.properties, total: _cache.properties.length, _stale: true });
    }

    // Tenter le fallback statique si disponible
    try {
      const fallback = require('../assets/data/properties-fallback.json');
      if (fallback && fallback.length > 0) {
        res.setHeader('Cache-Control', 'no-store');
        return res.status(200).json({ properties: fallback, total: fallback.length, _fallback: true });
      }
    } catch(e) { /* no fallback file */ }

    // Pas de cache — erreur propre (le CDN servira son stale-if-error)
    res.setHeader('Cache-Control', 'no-store');
    return res.status(503).json({ properties: [], total: 0, _error: err.message });
  }
};
