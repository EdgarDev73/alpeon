/**
 * GET /api/refresh-token          → refresh OAuth token (cron daily at 3h UTC)
 * GET /api/refresh-token?action=warm → warm Guesty cache
 *
 * Flow :
 * 1. OAuth → new Guesty token
 * 2. Save to Lambda memory + /tmp
 * 3. Update GUESTY_ACCESS_TOKEN env var in Vercel
 * 4. Trigger a Vercel redeploy → new cold-start Lambdas get the fresh token baked-in
 *    (évite l'invalidation du token par les anciens Lambdas encore chauds)
 */

const { getListings, normalizeListings, saveToken } = require('./_lib/guesty');

const OAUTH_URL         = 'https://booking.guesty.com/oauth2/token';
const SECRET            = process.env.REFRESH_SECRET;
const VERCEL_TOKEN      = process.env.VRL_API_TOKEN || process.env.VERCEL_TOKEN;
const VERCEL_PROJECT_ID = process.env.VERCEL_PROJECT_ID || 'prj_lkINpF7Y4ucOpVPDyEdAwJLefCaf';

/* ── Met à jour GUESTY_ACCESS_TOKEN dans les env vars Vercel ── */
async function updateVercelEnvVar(token) {
  if (!VERCEL_TOKEN) return { ok: false, reason: 'VERCEL_TOKEN not set' };
  try {
    // Essai PATCH direct (l'env var existe déjà)
    const list = await fetch(
      `https://api.vercel.com/v9/projects/${VERCEL_PROJECT_ID}/env`,
      { headers: { 'Authorization': `Bearer ${VERCEL_TOKEN}` } }
    ).then(x => x.json());
    const env = (list.envs || []).find(e => e.key === 'GUESTY_ACCESS_TOKEN');
    if (env) {
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
    // Fallback : créer l'env var
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
    return { ok: r.ok, status: r.status };
  } catch (e) {
    return { ok: false, reason: e.message };
  }
}

/* ── Déclenche un redéploiement Vercel (non-bloquant) ── */
async function triggerRedeploy() {
  if (!VERCEL_TOKEN) return { ok: false, reason: 'VERCEL_TOKEN not set' };
  try {
    // Récupérer le dernier déploiement production
    const deploys = await fetch(
      `https://api.vercel.com/v6/deployments?projectId=${VERCEL_PROJECT_ID}&target=production&limit=1`,
      { headers: { 'Authorization': `Bearer ${VERCEL_TOKEN}` } }
    ).then(r => r.json());
    const last = (deploys.deployments || [])[0];
    if (!last) return { ok: false, reason: 'no production deployment found' };

    // Redéployer avec les env vars fraîches
    const r = await fetch(
      `https://api.vercel.com/v13/deployments/${last.uid}/redeploy`,
      {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${VERCEL_TOKEN}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({ target: 'production' }),
      }
    );
    const body = await r.json();
    console.log('[refresh-token] Redeploy triggered:', body.id || body.url || r.status);
    return { ok: r.ok, status: r.status, deployment: body.id };
  } catch (e) {
    console.warn('[refresh-token] Redeploy failed (non-critical):', e.message);
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

    // Redéploiement en arrière-plan (non-bloquant) pour que les nouveaux Lambdas
    // démarrent avec le token frais baked-in dans leur process.env
    triggerRedeploy().catch(e => console.warn('[refresh-token] redeploy bg error:', e.message));

    const expiry = Date.now() + (json.expires_in || 86400) * 1000;
    return res.status(200).json({
      ok: true,
      expires: new Date(expiry).toISOString(),
      vercel_env_updated: vercelResult.ok,
    });
  } catch (err) {
    return res.status(500).json({ ok: false, error: err.message });
  }
};
