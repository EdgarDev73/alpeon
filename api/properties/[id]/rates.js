/**
 * GET /api/properties/[id]/rates?checkIn=YYYY-MM-DD&checkOut=YYYY-MM-DD
 * Returns per-night prices from Guesty nightlyRates for the given date range.
 */
const { getNightlyRates } = require('../../_lib/guesty');

module.exports = async (req, res) => {
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'GET') return res.status(405).json({ error: 'Method not allowed' });

  const { id, checkIn, startDate, checkOut, endDate } = req.query;
  if (!id) return res.status(400).json({ error: 'Missing listing id' });

  const from = checkIn || startDate;
  const to   = checkOut || endDate;
  if (!from || !to) return res.status(400).json({ error: 'Missing checkIn/checkOut' });

  try {
    const nightlyRates = await getNightlyRates(id, from, to);
    return res.status(200).json({ rates: nightlyRates || {} });
  } catch (err) {
    console.error('[/api/properties/rates]', err.message);
    return res.status(500).json({ error: err.message });
  }
};
