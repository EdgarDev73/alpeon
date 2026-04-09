/**
 * ALPÉON — Guesty Booking Engine API
 *
 * Architecture token (fix rate-limit structurel) :
 * ─────────────────────────────────────────────────
 * Les Lambdas user-facing (properties, calendar, etc.) ne font JAMAIS d'OAuth.
 * Elles lisent uniquement GUESTY_ACCESS_TOKEN depuis l'env Vercel.
 *
 * Seul /api/refresh-token (cron 3h + 15h) appelle OAuth et met à jour
 * GUESTY_ACCESS_TOKEN dans Vercel via l'API Vercel.
 *
 * En cas de token manquant/expiré → erreur 503 claire, jamais de flood OAuth.
 *
 * Required env vars (Vercel dashboard) :
 *   GUESTY_ACCESS_TOKEN   — mis à jour automatiquement par le cron
 *   GUESTY_CLIENT_ID      — utilisé uniquement par refresh-token
 *   GUESTY_CLIENT_SECRET  — utilisé uniquement par refresh-token
 */

const fs   = require('fs');
const path = require('path');

const BASE   = 'https://booking.guesty.com/api';
const ORIGIN = 'https://jupiter-residences.guestybookings.com';
const G_AID  = 'G-89C7E-9FB65-B6F69';

// /tmp survives entre requêtes sur une instance Lambda chaude
const TOKEN_FILE = '/tmp/.guesty_token.json';

/* ── Token en mémoire (instance chaude) ── */
let _mem = { token: null, expiry: 0 };

function _jwtExpiry(token) {
  try {
    const p = JSON.parse(Buffer.from(token.split('.')[1], 'base64url').toString());
    return (p.exp || 0) * 1000;
  } catch { return 0; }
}

/**
 * Retourne le meilleur token disponible sans jamais appeler OAuth.
 * Priorité : env var → cache /tmp → env var périmé (grace period Guesty)
 * Lance une erreur si aucun token utilisable.
 */
function getToken() {
  const envToken = process.env.GUESTY_ACCESS_TOKEN;

  // 1) Env var frais (5 min de marge)
  if (envToken && _jwtExpiry(envToken) > Date.now() + 300_000) {
    return envToken;
  }

  // 2) Cache mémoire frais
  if (_mem.token && _mem.expiry > Date.now() + 300_000) {
    return _mem.token;
  }

  // 3) Cache /tmp frais
  try {
    const { token, expiry } = JSON.parse(fs.readFileSync(TOKEN_FILE, 'utf8'));
    if (token && expiry > Date.now() + 300_000) {
      _mem = { token, expiry };
      return token;
    }
  } catch { /* pas de fichier */ }

  // 4) Env var légèrement périmé — Guesty honore souvent une grace period de quelques heures
  if (envToken) {
    const exp = _jwtExpiry(envToken);
    const staleMs = Date.now() - exp;
    if (staleMs < 4 * 3600_000) { // moins de 4h de retard
      console.warn(`[guesty] Token expiré depuis ${Math.round(staleMs/60000)}min — utilisation grace period`);
      return envToken;
    }
  }

  // 5) Cache /tmp périmé en dernier recours
  try {
    const { token } = JSON.parse(fs.readFileSync(TOKEN_FILE, 'utf8'));
    if (token) {
      console.warn('[guesty] Utilisation token /tmp périmé en dernier recours');
      return token;
    }
  } catch { /* pas de fichier */ }

  throw new Error('GUESTY_ACCESS_TOKEN manquant ou expiré — le cron refresh-token doit être exécuté');
}

/**
 * Sauvegarde un token frais en mémoire + /tmp.
 * Appelé uniquement par refresh-token.js après un OAuth réussi.
 */
function saveToken(token, expiresIn) {
  const expiry = Date.now() + (expiresIn || 86400) * 1000;
  _mem = { token, expiry };
  try { fs.writeFileSync(TOKEN_FILE, JSON.stringify({ token, expiry })); } catch { /* ignore */ }
}

/* ── Requête générique Guesty ── */
async function guestyFetch(apiPath, { method = 'GET', body, params } = {}) {
  const token = getToken(); // synchrone, jamais d'OAuth
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

  if (!res.ok) throw new Error(`Guesty ${method} ${apiPath} → ${res.status}: ${await res.text()}`);
  return res.json();
}

/* ── Listings ── */
async function getListings({ limit = 100 } = {}) {
  return guestyFetch('/listings', { params: { limit } });
}

/* ── Single listing ── */
async function getListing(id) {
  return guestyFetch(`/listings/${id}`);
}

/* ── Calendar ── */
async function getListingCalendar(listingId, { startDate, endDate } = {}) {
  const today  = new Date();
  const in180  = new Date(today.getTime() + 180 * 86_400_000);
  return guestyFetch(`/listings/${listingId}/calendar`, {
    params: {
      from: startDate || today.toISOString().slice(0, 10),
      to:   endDate   || in180.toISOString().slice(0, 10),
    },
  });
}

/* ── Nightly rates ── */
async function getNightlyRates(listingId, checkIn, checkOut) {
  const data    = await guestyFetch('/listings', { params: { checkIn, checkOut, limit: 100 } });
  const results = data.results || data.listings || data.data || (Array.isArray(data) ? data : []);
  const listing = results.find(l => l._id === listingId);
  return listing?.nightlyRates || null;
}

/* ── Quote ── */
async function createQuote({ listingId, checkIn, checkOut, guests }) {
  return guestyFetch('/quotes', {
    method: 'POST',
    body: { listingId, checkIn, checkOut, guestsCount: guests },
  });
}

/* ── Normalizer ── */
function normalizeListings(raw) {
  const results = raw.results || raw.listings || raw.data || (Array.isArray(raw) ? raw : []);
  return results.map(normalizeListing);
}

function normalizeListing(l) {
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
    image:           pics[0]?.original || pics[0]?.thumbnail || '',
    images:          pics.slice(0, 8).map(p => p.original || p.thumbnail).filter(Boolean),
    tags,
    bookingUrl:      `${ORIGIN}/en/listing/${l._id}`,
  };
}

module.exports = { getToken, saveToken, guestyFetch, getListings, getListing, getListingCalendar, getNightlyRates, createQuote, normalizeListings, normalizeListing };
