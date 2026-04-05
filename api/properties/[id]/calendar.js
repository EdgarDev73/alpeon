/**
 * GET /api/properties/[id]/calendar
 * Query params: startDate, endDate (YYYY-MM-DD)
 */
const { getListingCalendar } = require('../../_lib/guesty');

module.exports = async (req, res) => {
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'GET') return res.status(405).json({ error: 'Method not allowed' });

  const { id, startDate, endDate } = req.query;
  if (!id) return res.status(400).json({ error: 'Missing listing id' });

  try {
    const raw = await getListingCalendar(id, { startDate, endDate });
    console.log('[calendar raw sample]', JSON.stringify((raw.data || raw.days || raw || [])[0]));
    const rawDays = raw.data || raw.days || (Array.isArray(raw) ? raw : []);
    const days = rawDays.map(d => ({
      date: d.date || d.day,
      available: d.status === 'available',
      minNights: d.minNights || d.minimumNights || d.min_nights || 1,
      price: d.price || d.basePrice || d.nightly_price || null,
      currency: d.currency || 'EUR',
      status: d.status,
    }));
    return res.status(200).json({ days });
  } catch (err) {
    console.error('[/api/properties/calendar]', err.message);
    return res.status(500).json({ error: err.message });
  }
};
