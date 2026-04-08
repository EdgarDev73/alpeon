/**
 * GET /api/refresh-token
 * Fetches a fresh Guesty OAuth token and writes it to /tmp so future Lambda
 * invocations (same instance) can reuse it without calling OAuth again.
 *
 * Called by Vercel Cron every 20 hours — keeps the token perpetually fresh
 * without cold-start hammering.
 *
 * Protected by a simple secret so it's not publicly abusable.
 */

const fs   = require('fs');
const path = require('path');

const OAUTH_URL  = 'https://booking.guesty.com/oauth2/token';
const TOKEN_FILE = '/tmp/.guesty_token.json';
const LOCAL_FILE = path.join(__dirname, '_lib/.token_cache.json');
const SECRET     = process.env.REFRESH_SECRET;
if (!SECRET) console.warn('[refresh-token] REFRESH_SECRET env var not set');

module.exports = async (req, res) => {
  // Allow: Vercel cron (sets x-vercel-cron:1), or manual call with REFRESH_SECRET
  const isVercelCron = req.headers['x-vercel-cron'] === '1';
  const provided     = req.headers['x-refresh-secret'] || req.query.secret;
  if (!isVercelCron && provided !== SECRET) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  const id     = process.env.GUESTY_CLIENT_ID;
  const secret = process.env.GUESTY_CLIENT_SECRET;
  if (!id || !secret) return res.status(500).json({ ok: false, error: 'Missing GUESTY credentials env vars' });

  try {
    const r = await fetch(OAUTH_URL, {
      method:  'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body:    new URLSearchParams({ grant_type: 'client_credentials', client_id: id, client_secret: secret }),
    });
    if (!r.ok) {
      const txt = await r.text();
      throw new Error(`OAuth failed ${r.status}: ${txt}`);
    }
    const json    = await r.json();
    const token   = json.access_token;
    const expiry  = Date.now() + (json.expires_in || 86400) * 1000;
    const payload = JSON.stringify({ token, expiry });

    // Write to both /tmp and __dirname (best-effort)
    for (const f of [TOKEN_FILE, LOCAL_FILE]) {
      try { fs.writeFileSync(f, payload); } catch { /* ignore */ }
    }

    return res.status(200).json({
      ok: true,
      expires: new Date(expiry).toISOString(),
      token_preview: token.slice(0, 20) + '...',
    });
  } catch (err) {
    return res.status(500).json({ ok: false, error: err.message });
  }
};
