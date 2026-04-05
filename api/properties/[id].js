/**
 * GET /api/properties/:id
 * Returns a single Guesty listing, normalised.
 */
const { getListing, normalizeListing } = require('../_lib/guesty');

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'GET') return res.status(405).json({ error: 'Method not allowed' });

  const id = req.query.id;
  if (!id) return res.status(400).json({ error: 'Missing id' });

  try {
    const raw = await getListing(id);
    return res.status(200).json({ property: normalizeListing(raw) });
  } catch (err) {
    console.error('[properties/[id]]', err.message);
    return res.status(500).json({ error: err.message });
  }
};
