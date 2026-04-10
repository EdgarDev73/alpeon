/**
 * GET /api/refresh-token          → refresh OAuth token (cron 4h daily)
 * GET /api/refresh-token?action=warm → warm Guesty cache
 */

const { getListings, normalizeListings, saveToken } = require('./_lib/guesty');

const OAUTH_URL         = 'https://booking.guesty.com/oauth2/token';
const SECRET            = process.env.REFRESH_SECRET;
const VERCEL_TOKEN      = process.env.VRL_API_TOKEN || process.env.VERCEL_TOKEN;
const VERCEL_PROJECT_ID = process.env.VERCEL_PROJECT_ID || 'prj_lkINpF7Y4ucOpVPDyEdAwJLefCaf';

async function updateVercelEnvVar(token) {
  if (!VERCEL_TOKEN) return { ok: false, reason: 'VERCEL_TOKEN not set' };
  try {
    const r = await fetch(
      `https://api.vercel.com/v9/projects/${VERCEL_PROJECT_ID}/env`,
      {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${VERCEL_TOKEN}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({
          key: 'GUESTY_ACCESS_TOKEN', value: token, type: 'encrypted',
          target: ['production', 'preview', 'development'],
        }),
      }
    );
    if (r.status === 403 || r.status === 409) {
      const list = await fetch(
        `https://api.vercel.com/v9/projects/${VERCEL_PROJECT_ID}/env`,
        { headers: { 'Authorization': `Bearer ${VERCEL_TOKEN}` } }
      ).then(x => x.json());
      const env = (list.envs || []).find(e => e.key === 'GUESTY_ACCESS_TOKEN');
      if (!env) return { ok: false, reason: 'env var not found after conflict' };
      const patch = await fetch(
        `https://api.vercel.com/v9/projects/${VERCEL_PROJECT_ID}/env/${env.id}`,
        {
          method: 'PATCH',
          headers: { 'Authorization': `Bearer ${VERCEL_TOKEN}`, 'Content-Type': 'application/json' },
          body: JSON.stringify({ value: token, target: ['production', 'preview', 'development'] }),
        }
      );
      return { ok: patch.ok, status: patch.status };
    }
    return { ok: r.ok, status: r.status };
  } catch (e) {
    return { ok: false, reason: e.message };
  }
}

async function handleWarm(req, res) {
  const isVercelCron = req.headers['x-vercel-cron'] === '1';
  const secret = req.headers['x-warm-secret'] || req.query.secret;
  if (!isVercelCron && secret !== process.env.REFRESH_SECRET) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  const start = Date.now();
  try {
    const raw = await getListings({ limit: 100 });
    const properties = normalizeListings(raw);
    console.log(`[warm-cache] ${properties.length} propriétés chargées depuis Guesty`);
    res.setHeader('Cache-Control', 'no-store');
    return res.status(200).json({
      ok: true,
      properties: properties.length,
      listings: properties.map(p => p.id),
      cached_at: new Date().toISOString(),
      duration_ms: Date.now() - start,
    });
  } catch (err) {
    console.error('[warm-cache] Erreur:', err.message);
    res.setHeader('Cache-Control', 'no-store');
    return res.status(500).json({ ok: false, error: err.message, duration_ms: Date.now() - start });
  }
}

module.exports = async (req, res) => {
  if (req.query.action === 'warm') return handleWarm(req, res);

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
    if (!r.ok) throw new Error(`OAuth failed ${r.status}: ${await r.text()}`);

    const json  = await r.json();
    const token = json.access_token;

    saveToken(token, json.expires_in);
    const vercelResult = await updateVercelEnvVar(token);
    console.log('[refresh-token] Vercel env var update:', vercelResult);

    const expiry = Date.now() + (json.expires_in || 86400) * 1000;
    return res.status(200).json({
      ok: true,
      expires: new Date(expiry).toISOString(),
      access_token: token,
      vercel_env_updated: vercelResult.ok,
    });
  } catch (err) {
    return res.status(500).json({ ok: false, error: err.message });
  }
};
