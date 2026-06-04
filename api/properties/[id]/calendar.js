/**
 * GET /api/properties/[id]/calendar
 * Query params: startDate, endDate (YYYY-MM-DD)
 *
 * Cache mémoire Lambda 30 min + stale-if-error : en cas d'erreur Guesty
 * on sert le dernier calendrier connu plutôt qu'une 500.
 */
const { getListingCalendar } = require('../../_lib/guesty');

const _cache = new Map(); // `${id}:${startDate}:${endDate}` → { days, fetchedAt }
const CACHE_TTL = 30 * 60 * 1000; // 30 min

module.exports = async (req, res) => {
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'GET') return res.status(405).json({ error: 'Method not allowed' });

  const { id, startDate, endDate } = req.query;
  if (!id) return res.status(400).json({ error: 'Missing listing id' });

  const cacheKey = `${id}:${startDate || ''}:${endDate || ''}`;
  const cached   = _cache.get(cacheKey);
  const now      = Date.now();

  try {
    // Servir depuis le cache mémoire si frais
    if (cached && now - cached.fetchedAt < CACHE_TTL) {
      res.setHeader('Cache-Control', 's-maxage=1800, stale-while-revalidate=300, stale-if-error=86400');
      return res.status(200).json({ days: cached.days });
    }

    const raw = await getListingCalendar(id, { startDate, endDate });
    const rawDays = Array.isArray(raw) ? raw : (raw.data || raw.days || []);
    if (!rawDays.length) console.warn('[calendar] empty response from Guesty for listing', id);

    const days = rawDays.map(d => ({
      date:      d.date || d.day,
      available: d.status === 'available',
      minNights: d.minNights || d.minimumNights || d.min_nights || 1,
      price:     d.price || d.basePrice || d.nightly_price || null,
      currency:  d.currency || 'EUR',
      status:    d.status,
      cta:       d.cta || false,
      ctd:       d.ctd || false,
    }));

    _cache.set(cacheKey, { days, fetchedAt: now });
    res.setHeader('Cache-Control', 's-maxage=1800, stale-while-revalidate=300, stale-if-error=86400');
    return res.status(200).json({ days });

  } catch (err) {
    console.error('[calendar]', id, err.message);

    // 1. Stale cache → toujours servir en priorité
    if (cached) {
      console.warn('[calendar] serving stale cache after error for', id);
      res.setHeader('Cache-Control', 'no-store');
      return res.status(200).json({ days: cached.days, _stale: true });
    }

    // 2. Pas de cache : retourner 200 avec tableau vide plutôt qu'une 500.
    // L'UI affiche "disponibilité non chargée" au lieu de planter.
    // Un 401 répété = listing non accessible via Booking Engine (pb Guesty config).
    const is401 = err.message.includes('401');
    console.warn(`[calendar] no cache, returning empty days (${is401 ? '401-permanent' : 'error'})`);
    res.setHeader('Cache-Control', 'no-store');
    return res.status(200).json({ days: [], _unavailable: true });
  }
};
