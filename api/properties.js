/**
 * GET /api/properties
 * Returns live Guesty Booking Engine listings, normalised for ALPÉON UI.
 */

const { getListings, normalizeListings } = require('./_lib/guesty');

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'GET') return res.status(405).json({ error: 'Method not allowed' });

  const { city, type, guests, limit = '100' } = req.query;

  try {
    const raw = await getListings({ limit: parseInt(limit) });
    let properties = normalizeListings(raw);

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

    // Cache-Control strategy:
    // - s-maxage=60        : Vercel edge serves fresh data for 60s
    // - stale-while-revalidate=3600 : revalidate in background, serve stale for up to 1h
    // - stale-if-error=86400       : if Guesty is down, serve last good response for 24h
    res.setHeader('Cache-Control', 's-maxage=60, stale-while-revalidate=3600, stale-if-error=86400');
    return res.status(200).json({ properties, total: properties.length });
  } catch (err) {
    console.error('[properties] Guesty error:', err.message);
    // Return a valid 200 so stale-if-error CDN cache kicks in on next request
    // (CDN will serve last cached good response instead of this fallback)
    res.setHeader('Cache-Control', 'no-store');
    return res.status(200).json({ properties: [], total: 0, _error: err.message });
  }
};
