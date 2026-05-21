/**
 * GET /api/debug-listing?id=<listingId>
 * Returns raw Guesty fields for one listing — TEMP DEBUG, remove after use.
 */
const { guestyFetch } = require('./_lib/guesty');

module.exports = async (req, res) => {
  if (req.method !== 'GET') return res.status(405).end();
  const id = req.query.id;
  if (!id) return res.status(400).json({ error: 'Missing id' });
  try {
    const raw = await guestyFetch(`/listings/${id}`);
    // Return only name-like fields + a few key ones
    const nameFields = Object.keys(raw).filter(k =>
      ['name','title','nick','label','intern','alias','private','room'].some(kw => k.toLowerCase().includes(kw))
    );
    const out = { allKeys: Object.keys(raw).sort(), nameFields: {} };
    nameFields.forEach(k => out.nameFields[k] = raw[k]);
    return res.status(200).json(out);
  } catch(e) {
    return res.status(500).json({ error: e.message });
  }
};
