/**
 * ALPÉON — Guesty Booking Engine API
 * Token: POST https://booking.guesty.com/oauth2/token  (client_credentials)
 * API:   GET  https://booking.guesty.com/api/listings
 * Required headers: g-aid-cs + Origin (booking engine origin)
 */

const fs        = require('fs');
const path      = require('path');

const OAUTH_URL  = 'https://booking.guesty.com/oauth2/token';
const BASE       = 'https://booking.guesty.com/api';
const ORIGIN     = 'https://jupiter-residences.guestybookings.com';
const G_AID_CS   = 'G-89C7E-9FB65-B6F69';
const TOKEN_FILE = path.join(__dirname, '.token_cache.json');

/* ── Token cache (in-memory + file, survives restarts in dev) ── */
let _cachedToken = null;
let _tokenExpiry  = 0;

function _loadTokenCache() {
  if (_cachedToken) return;
  try {
    const raw = fs.readFileSync(TOKEN_FILE, 'utf8');
    const { token, expiry } = JSON.parse(raw);
    if (token && expiry > Date.now()) { _cachedToken = token; _tokenExpiry = expiry; }
  } catch { /* no cache file yet */ }
}

function _saveTokenCache() {
  try { fs.writeFileSync(TOKEN_FILE, JSON.stringify({ token: _cachedToken, expiry: _tokenExpiry })); }
  catch { /* ignore write errors (e.g. read-only lambda) */ }
}

function _jwtExpiry(token) {
  try {
    const payload = JSON.parse(Buffer.from(token.split('.')[1], 'base64').toString());
    return (payload.exp || 0) * 1000; // ms
  } catch { return 0; }
}

async function getToken() {
  // 1) Static token from env var — only use if not expired (5 min safety margin)
  const staticToken = process.env.GUESTY_ACCESS_TOKEN;
  if (staticToken && _jwtExpiry(staticToken) > Date.now() + 300_000) {
    return staticToken;
  }

  // 2) In-memory / file cache
  _loadTokenCache();
  if (_cachedToken && Date.now() < _tokenExpiry - 300_000) return _cachedToken;

  const id     = process.env.GUESTY_CLIENT_ID     || '0oatxyy1lnqP1Rlwu5d7';
  const secret = process.env.GUESTY_CLIENT_SECRET || '7LG2doVNI25O-1ekKfwkNwW-grUWy5kSZobsL1h_a2yBqvz4j-hgj_mP_9TiMyKk';
  if (!id || !secret) throw new Error('Missing GUESTY_CLIENT_ID / GUESTY_CLIENT_SECRET');

  // 3) OAuth with retry + backoff (handles 429 on Vercel cold-start bursts)
  let lastErr;
  for (let attempt = 0; attempt < 5; attempt++) {
    if (attempt > 0) await new Promise(r => setTimeout(r, 1000 * Math.pow(2, attempt - 1)));
    const oauthCtrl = new AbortController();
    const oauthTimer = setTimeout(() => oauthCtrl.abort(), 5000);
    let res;
    try {
      res = await fetch(OAUTH_URL, {
        method:  'POST',
        signal:  oauthCtrl.signal,
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body:    new URLSearchParams({ grant_type: 'client_credentials', client_id: id, client_secret: secret }),
      });
    } finally {
      clearTimeout(oauthTimer);
    }
    if (res.status === 429) { lastErr = new Error('Guesty OAuth rate-limited (429)'); continue; }
    if (!res.ok) throw new Error(`Guesty OAuth failed ${res.status}: ${await res.text()}`);
    const json   = await res.json();
    _cachedToken = json.access_token;
    _tokenExpiry = Date.now() + (json.expires_in || 86400) * 1000;
    _saveTokenCache();
    return _cachedToken;
  }
  throw lastErr;
}

/* ── Generic request ── */
async function guestyFetch(path, { method = 'GET', body, params } = {}) {
  const token = await getToken();
  let url = `${BASE}${path}`;
  if (params) {
    const qs = new URLSearchParams(
      Object.entries(params).filter(([, v]) => v != null)
    ).toString();
    if (qs) url += `?${qs}`;
  }
  // 8s timeout — Vercel functions max out at 10s, never let Guesty hang the whole request
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
        'g-aid-cs':      G_AID_CS,
        'Origin':        ORIGIN,
        'Referer':       `${ORIGIN}/en`,
      },
      ...(body ? { body: JSON.stringify(body) } : {}),
    });
  } finally {
    clearTimeout(timer);
  }
  if (!res.ok) throw new Error(`Guesty ${method} ${path} → ${res.status}: ${await res.text()}`);
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
  const today = new Date();
  const in180 = new Date(today.getTime() + 180 * 86_400_000);
  return guestyFetch(`/listings/${listingId}/calendar`, {
    params: {
      from: startDate || today.toISOString().slice(0, 10),
      to:   endDate   || in180.toISOString().slice(0, 10),
    },
  });
}

/* ── Nightly rates for a specific listing + date range ── */
async function getNightlyRates(listingId, checkIn, checkOut) {
  // Guesty returns nightlyRates only via the /listings list endpoint with checkIn/checkOut
  const data = await guestyFetch('/listings', { params: { checkIn, checkOut, limit: 100 } });
  const results = data.results || data.listings || data.data || (Array.isArray(data) ? data : []);
  const listing = results.find(l => l._id === listingId);
  return listing?.nightlyRates || null; // null = listing not available for these dates
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
  const addr  = l.address  || {};
  const price = l.prices   || {};
  const pics  = l.pictures || [];
  const desc  = l.publicDescription || {};
  const reviews = l.reviews || {};

  const pt = (l.propertyType || '').toLowerCase();
  const propertyType = pt.includes('chalet') ? 'chalet'
    : pt.includes('apart') || pt.includes('apt') ? 'appartement'
    : pt.includes('penthouse') ? 'penthouse'
    : 'appartement';

  const tags = [];
  if ((l.tags || []).includes('Luxe')) tags.push('Prestige');
  if ((l.accommodates || 0) >= 10) tags.push('Grand groupe');

  // Guesty reviews avg is 0–10, convert to 0–5
  const avg = reviews.avg || 0;
  const rating = avg ? Math.round((avg / 10 * 5) * 10) / 10 : 0;

  const PRIORITY = ['Sauna','Hot tub','Pool','Gym','Cinema','fireplace','Ski','Parking','Wifi','Wireless','Dishwasher','Washer','Dryer','Elevator','Family'];
  const amenities = (l.amenities || [])
    .filter(a => PRIORITY.some(p => a.toLowerCase().includes(p.toLowerCase())))
    .slice(0, 5);

  return {
    id:           l._id,
    title:        (l.title || l.nickname || '').trim(),
    city:         addr.city || '',
    area:         addr.neighborhood || '',
    country:      addr.country || 'France',
    propertyType,
    guests:       l.accommodates || 0,
    bedrooms:     l.bedrooms  || 0,
    bathrooms:    l.bathrooms || 0,
    priceFrom:    price.basePrice || price.weeklyRate || 0,
    currency:     price.currency || 'EUR',
    rating,
    reviewsCount: reviews.total || 0,
    summary:      (typeof desc === 'object' ? desc.summary : desc || '').replace(/\n- /g, ' ').replace(/^- /,'').trim().slice(0, 220),
    fullDescription: (typeof desc === 'object' ? (desc.summary || '') + (desc.space ? '\n\n' + desc.space : '') + (desc.access ? '\n\n' + desc.access : '') : desc || '').trim(),
    amenities,
    allAmenities: l.amenities || [],
    image:        pics[0]?.original || pics[0]?.thumbnail || '',
    images:       pics.slice(0, 8).map(p => p.original || p.thumbnail).filter(Boolean),
    tags,
    bookingUrl:   `${ORIGIN}/en/listing/${l._id}`,
  };
}

module.exports = { getToken, guestyFetch, getListings, getListing, getListingCalendar, getNightlyRates, createQuote, normalizeListings, normalizeListing };
