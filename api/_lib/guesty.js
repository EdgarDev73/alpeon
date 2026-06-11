/**
 * ALPÉON — Guesty Booking Engine API
 *
 * Architecture token (self-healing) :
 * ─────────────────────────────────────────────────
 * getToken() est async et rafraîchit le token automatiquement si expiré.
 * Plus jamais de 503 dû à un token expiré.
 *
 * Priorité : env var frais → mémoire → /tmp → OAuth auto (fallback)
 *
 * Un cooldown de 60s évite de flooder OAuth sur des requêtes concurrentes.
 *
 * Required env vars (Vercel dashboard) :
 *   GUESTY_CLIENT_ID      — pour OAuth
 *   GUESTY_CLIENT_SECRET  — pour OAuth
 *   GUESTY_ACCESS_TOKEN   — mis à jour par le cron ET par getToken() auto
 *   VRL_API_TOKEN         — pour mettre à jour l'env Vercel après refresh
 */

const fs = require('fs');

const BASE             = 'https://booking.guesty.com/api';
const OAUTH_URL        = 'https://booking.guesty.com/oauth2/token';
const ORIGIN           = 'https://jupiter-residences.guestybookings.com';
const G_AID            = 'G-89C7E-9FB65-B6F69';
const TOKEN_FILE       = '/tmp/.guesty_token.json';
const VERCEL_PROJECT_ID = process.env.VERCEL_PROJECT_ID || 'prj_lkINpF7Y4ucOpVPDyEdAwJLefCaf';

/* ── Cache mémoire (instance Lambda chaude) ── */
let _mem = { token: null, expiry: 0 };

function _jwtExpiry(token) {
  try {
    const p = JSON.parse(Buffer.from(token.split('.')[1], 'base64url').toString());
    return (p.exp || 0) * 1000;
  } catch { return 0; }
}

function saveToken(token, expiresIn) {
  const expiry = Date.now() + (expiresIn || 86400) * 1000;
  _mem = { token, expiry };
  try { fs.writeFileSync(TOKEN_FILE, JSON.stringify({ token, expiry })); } catch { /* ignore */ }
}

/**
 * Retourne le meilleur token disponible — SANS JAMAIS faire d'OAuth.
 *
 * ⚠️ RÈGLE ABSOLUE : les Lambdas API (properties, calendar, quotes…) ne font
 * JAMAIS d'appel OAuth. L'OAuth est rate-limité TRÈS agressivement par Guesty :
 * si N Lambdas froids tentent OAuth en même temps quand le token expire, Guesty
 * bloque (429) le client OAUTH ENTIER — y compris le cron — et il faut alors
 * recréer une nouvelle application Guesty. C'est LA cause des pannes quotidiennes.
 *
 * Le SEUL composant autorisé à faire OAuth est /api/refresh-token (cron 6h),
 * qui fait 1 appel toutes les 6h = 4/jour → jamais rate-limité.
 *
 * Ici on retourne simplement le token le plus frais qu'on ait sous la main.
 * S'il est expiré, Guesty renverra 401 et l'appelant servira son cache/stale.
 * On ne tente RIEN pour le rafraîchir — c'est le boulot du cron.
 *
 * Ordre : 1) mémoire  2) /tmp  3) env var baked-in (même expirée)
 */
async function getToken() {
  // 1) Cache mémoire (instance chaude — ex: après que le cron ait fait saveToken)
  if (_mem.token) return _mem.token;

  // 2) Cache /tmp (instance réchauffée)
  try {
    const { token } = JSON.parse(fs.readFileSync(TOKEN_FILE, 'utf8'));
    if (token) { _mem.token = token; return token; }
  } catch { /* pas de fichier */ }

  // 3) Env var baked-in au deploy — utilisée même si expirée.
  //    Guesty renverra 401 si périmée → l'appelant sert son cache/stale.
  const envToken = process.env.GUESTY_ACCESS_TOKEN;
  if (envToken) {
    const remainMs = _jwtExpiry(envToken) - Date.now();
    if (remainMs <= 0) {
      console.warn(`[guesty] Env token expiré depuis ${Math.round(-remainMs/3600000)}h — le cron /api/refresh-token doit le renouveler`);
    }
    return envToken;
  }

  throw new Error('Aucun token Guesty disponible (le cron /api/refresh-token doit le renouveler)');
}

/* ── Requête générique Guesty ── */
async function guestyFetch(apiPath, { method = 'GET', body, params } = {}) {
  const token = await getToken();
  let url = `${BASE}${apiPath}`;
  if (params) {
    const qs = new URLSearchParams(
      Object.entries(params).filter(([, v]) => v != null)
    ).toString();
    if (qs) url += `?${qs}`;
  }

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 8000);

  let res;
  try {
    res = await fetch(url, {
      method,
      signal: controller.signal,
      headers: {
        'Accept':        'application/json',
        'Content-Type':  'application/json',
        'Authorization': `Bearer ${token}`,
        'g-aid-cs':      G_AID,
        'Origin':        ORIGIN,
        'Referer':       `${ORIGIN}/en`,
      },
      ...(body ? { body: JSON.stringify(body) } : {}),
    });
  } finally {
    clearTimeout(timer);
  }

  // 401 = token périmé. On NE fait PAS d'OAuth ici (cause du thundering herd
  // → 429 → client OAuth bloqué). On vide juste le cache mémoire/tmp pour que
  // la prochaine instance reparte de l'env var, et on remonte l'erreur :
  // l'appelant (properties.js / calendar.js) sert alors son cache ou un fallback.
  // C'est le cron /api/refresh-token qui renouvellera le token.
  if (res.status === 401) {
    console.warn('[guesty] 401 on', apiPath, '— token périmé, le cron doit le renouveler (pas d\'OAuth Lambda)');
    _mem = { token: null, expiry: 0 };
    try { fs.unlinkSync(TOKEN_FILE); } catch { /* ignore */ }
  }

  if (!res.ok) throw new Error(`Guesty ${method} ${apiPath} → ${res.status}: ${await res.text()}`);
  return res.json();
}

/* ── Listings — pagination par curseur (Guesty Booking Engine) ── */
async function getListings({ limit = 100, checkIn, checkOut } = {}) {
  const PAGE_SIZE = 25;
  let allResults = [];
  let meta       = {};

  // Première page
  const first = await guestyFetch('/listings', { params: { limit: PAGE_SIZE, checkIn, checkOut } });
  meta = first;
  const page1 = first.results || first.listings || first.data || (Array.isArray(first) ? first : []);
  allResults = [...page1];

  // Guesty Booking Engine renvoie parfois total = PAGE_SIZE (pas le vrai total global).
  // On ne s'y fie pas pour arrêter la boucle — on suit le cursor jusqu'à ce qu'il soit null.
  const total = first.pagination?.total || first.total || first.count || Infinity;
  console.log(`[guesty] Page 1 → ${page1.length} listings (pagination.total: ${total === Infinity ? '?' : total})`);

  // Pages suivantes via curseur — on s'arrête sur cursor null ou limite atteinte
  let nextCursor = first.pagination?.cursor?.next || null;
  let pageNum = 1;

  while (nextCursor && allResults.length < limit) {
    pageNum++;
    try {
      const page = await guestyFetch('/listings', { params: { limit: PAGE_SIZE, cursor: nextCursor, checkIn, checkOut } });
      const rows = page.results || page.listings || page.data || (Array.isArray(page) ? page : []);
      if (!rows.length) break;
      allResults = [...allResults, ...rows];
      nextCursor = page.pagination?.cursor?.next || null;
      console.log(`[guesty] Page ${pageNum} → +${rows.length} (total: ${allResults.length})`);
    } catch (e) {
      console.warn(`[guesty] Pagination cursor page=${pageNum} échouée:`, e.message);
      break;
    }
  }

  console.log(`[guesty] getListings final: ${allResults.length}`);
  return { ...meta, results: allResults };
}

/* ── Single listing ── */
async function getListing(id) {
  return guestyFetch(`/listings/${id}`);
}

/* ── Calendar ── */
async function getListingCalendar(listingId, { startDate, endDate } = {}) {
  const today = new Date();
  const in365 = new Date(today.getTime() + 365 * 86_400_000);
  return guestyFetch(`/listings/${listingId}/calendar`, {
    params: {
      from: startDate || today.toISOString().slice(0, 10),
      to:   endDate   || in365.toISOString().slice(0, 10),
    },
  });
}

/* ── Nightly rates — via /reservations/quotes (accurate per-night pricing) ── */
async function getNightlyRates(listingId, checkIn, checkOut) {
  try {
    const quote = await guestyFetch('/reservations/quotes', {
      method: 'POST',
      body: {
        listingId,
        checkInDateLocalized:  checkIn,
        checkOutDateLocalized: checkOut,
        guestsCount: 2,
      },
    });
    const money  = quote?.rates?.ratePlans?.[0]?.ratePlan?.money || {};
    const accom  = money.fareAccommodationAdjusted || money.fareAccommodation || 0;
    const nights = Math.round((new Date(checkOut) - new Date(checkIn)) / 86_400_000);
    if (!accom || !nights) return null;

    // Build a per-night map (evenly distributed — Guesty doesn't expose nightly breakdown here)
    const perNight = Math.round((accom / nights) * 100) / 100;
    const map = {};
    let cur = new Date(checkIn);
    for (let i = 0; i < nights; i++) {
      map[cur.toISOString().slice(0, 10)] = perNight;
      cur = new Date(cur.getTime() + 86_400_000);
    }
    return map;
  } catch (e) {
    console.warn('[getNightlyRates] Quote failed:', e.message);
    return null;
  }
}

/* ── Quote ── */
async function createQuote({ listingId, checkIn, checkOut, guests }) {
  return guestyFetch('/quotes', {
    method: 'POST',
    body: { listingId, checkIn, checkOut, guestsCount: guests },
  });
}

/* ── Cloudinary WebP transform helper ── */
function transformImg(url, w) {
  if (!url || !url.includes('image/upload/')) return url;
  return url.replace('image/upload/', `image/upload/f_webp,q_auto:good,w_${w}/`);
}

/* ── Normalizer ── */
function normalizeListings(raw) {
  const results = raw.results || raw.listings || raw.data || (Array.isArray(raw) ? raw : []);
  return results.map(normalizeListing);
}

let _loggedFields = false;
function normalizeListing(l) {
  // Log raw field names once to identify the "internal name" field
  if (!_loggedFields) {
    _loggedFields = true;
    const nameFields = Object.keys(l).filter(k =>
      k.toLowerCase().includes('name') || k.toLowerCase().includes('title') ||
      k.toLowerCase().includes('nick') || k.toLowerCase().includes('label') ||
      k.toLowerCase().includes('intern') || k.toLowerCase().includes('alias')
    );
    console.log('[guesty] Raw name-like fields:', JSON.stringify(nameFields));
    console.log('[guesty] Sample values:', JSON.stringify(
      nameFields.reduce((o, k) => { o[k] = l[k]; return o; }, {})
    ));
  }

  const addr    = l.address  || {};
  const price   = l.prices   || {};
  const pics    = l.pictures || [];
  const desc    = l.publicDescription || {};
  const reviews = l.reviews  || {};

  const pt = (l.propertyType || '').toLowerCase();
  const propertyType = pt.includes('chalet') ? 'chalet'
    : pt.includes('apart') || pt.includes('apt') ? 'appartement'
    : pt.includes('penthouse') ? 'penthouse'
    : 'appartement';

  const tags = [];
  if ((l.tags || []).includes('Luxe')) tags.push('Signatures');
  if ((l.accommodates || 0) >= 10) tags.push('Grand groupe');

  const avg    = reviews.avg || 0;
  const rating = avg ? Math.round((avg / 10 * 5) * 10) / 10 : 0;

  const PRIORITY = ['Sauna','Hot tub','Pool','Gym','Cinema','fireplace','Ski','Parking','Wifi','Wireless','Dishwasher','Washer','Dryer','Elevator','Family'];
  const amenities = (l.amenities || [])
    .filter(a => PRIORITY.some(p => a.toLowerCase().includes(p.toLowerCase())))
    .slice(0, 5);

  const titleSlug = (l.title || l.nickname || '')
    .toLowerCase()
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9\s-]/g, '')
    .trim().replace(/\s+/g, '-')
    .replace(/-+/g, '-').slice(0, 60);
  const citySlug = (addr.city || '')
    .toLowerCase()
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9]/g, '-').replace(/-+/g, '-').replace(/^-|-$/g, '');
  const slug = citySlug ? `${titleSlug}-${citySlug}` : titleSlug;

  return {
    id:              l._id,
    slug,
    title:           (l.title || l.nickname || '').trim(),
    city:            addr.city || '',
    area:            addr.neighborhood || '',
    country:         addr.country || 'France',
    propertyType,
    guests:          l.accommodates || 0,
    bedrooms:        l.bedrooms  || 0,
    bathrooms:       l.bathrooms || 0,
    priceFrom:       price.basePrice || price.weeklyRate || 0,
    currency:        price.currency || 'EUR',
    rating,
    reviewsCount:    reviews.total || 0,
    summary:         (typeof desc === 'object' ? desc.summary : desc || '').replace(/\n- /g, ' ').replace(/^- /,'').trim().slice(0, 220),
    fullDescription: (typeof desc === 'object' ? (desc.summary || '') + (desc.space ? '\n\n' + desc.space : '') + (desc.access ? '\n\n' + desc.access : '') : desc || '').trim(),
    amenities,
    allAmenities:    l.amenities || [],
    image:           transformImg(pics[0]?.original || pics[0]?.thumbnail || '', 800),
    imageLg:         transformImg(pics[0]?.original || pics[0]?.thumbnail || '', 1400),
    images:          pics.slice(0, 20).map(p => transformImg(p.original || p.thumbnail, 1400)).filter(Boolean),
    tags,
    nickname:        l.nickname || '',
    bookingUrl:      `${ORIGIN}/en/listing/${l._id}`,
  };
}

module.exports = { getToken, saveToken, guestyFetch, getListings, getListing, getListingCalendar, getNightlyRates, createQuote, normalizeListings, normalizeListing };
