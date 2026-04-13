/* ──────────────────────────────────────────────────────────────────
   /api/lead  — Reçoit le payload de l'estimateur (ou tout lead)
   et le transmet au webhook Zapier configuré côté serveur.
   Utilise process.env.ZAPIER_ESTIMATEUR_WEBHOOK
────────────────────────────────────────────────────────────────── */
module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const payload = req.body || {};
  const ZAPIER_URL = process.env.ZAPIER_ESTIMATEUR_WEBHOOK;

  if (!ZAPIER_URL) {
    console.warn('[lead] ZAPIER_ESTIMATEUR_WEBHOOK non défini — lead non transmis');
    return res.status(200).json({ ok: true, dev: true });
  }

  try {
    await fetch(ZAPIER_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return res.status(200).json({ ok: true });
  } catch (e) {
    console.error('[lead] Zapier webhook error:', e.message);
    return res.status(200).json({ ok: true, _error: 'zapier_failed' });
  }
};
