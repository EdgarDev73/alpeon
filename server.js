/**
 * ALPÉON — Dev server local
 * Sert les fichiers statiques + les fonctions /api/*.js
 */
const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

// Auto-load env vars from .claude/launch.json if not already set
try {
  const launchJson = JSON.parse(fs.readFileSync(path.join(__dirname, '.claude', 'launch.json'), 'utf8'));
  const envVars = launchJson?.configurations?.[0]?.env || {};
  for (const [k, v] of Object.entries(envVars)) {
    if (!process.env[k]) process.env[k] = v;
  }
} catch (_) {}

const PORT = 3000;
const ROOT = __dirname;

const MIME = {
  '.html': 'text/html;charset=utf-8',
  '.css':  'text/css',
  '.js':   'application/javascript',
  '.json': 'application/json',
  '.png':  'image/png',
  '.jpg':  'image/jpeg',
  '.svg':  'image/svg+xml',
  '.ico':  'image/x-icon',
  '.mp4':  'video/mp4',
  '.woff2':'font/woff2',
};

const server = http.createServer(async (req, res) => {
  const parsed = url.parse(req.url, true);
  let pathname = parsed.pathname.replace(/\/$/, '') || '/';

  // CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,POST,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type,Authorization');
  if (req.method === 'OPTIONS') { res.writeHead(204); res.end(); return; }

  // === API routes ===
  if (pathname.startsWith('/api/')) {
    try {
      // Remove leading slash, map to file
      let apiPath = pathname.replace(/^\//, '');
      let handlerFile;

      // /api/properties/[id]/calendar → api/properties/[id]/calendar.js
      // /api/properties/[id]/rates   → api/properties/[id]/rates.js
      const calMatch   = pathname.match(/^\/api\/properties\/([^/]+)\/calendar$/);
      const ratesMatch = pathname.match(/^\/api\/properties\/([^/]+)\/rates$/);
      const propMatch  = pathname.match(/^\/api\/properties\/([^/]+)$/);
      if (calMatch) {
        handlerFile = path.join(ROOT, 'api', 'properties', '[id]', 'calendar.js');
        req.query = Object.assign({ id: calMatch[1] }, parsed.query);
      } else if (ratesMatch) {
        handlerFile = path.join(ROOT, 'api', 'properties', '[id]', 'rates.js');
        req.query = Object.assign({ id: ratesMatch[1] }, parsed.query);
      } else if (propMatch) {
        handlerFile = path.join(ROOT, 'api', 'properties', '[id].js');
        req.query = Object.assign({ id: propMatch[1] }, parsed.query);
      } else {
        // /api/properties → api/properties.js
        // /api/quote     → api/quote.js
        const segments = apiPath.split('/'); // ['api', 'properties']
        handlerFile = path.join(ROOT, ...segments) + '.js';
        req.query = Object.assign({}, parsed.query);
      }

      if (!fs.existsSync(handlerFile)) {
        res.writeHead(404, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: `Route not found: ${pathname}` }));
        return;
      }

      // Body parsing for POST
      if (req.method === 'POST') {
        const chunks = [];
        for await (const chunk of req) chunks.push(chunk);
        try { req.body = JSON.parse(Buffer.concat(chunks).toString()); }
        catch { req.body = {}; }
      }

      // Build response helper
      let statusCode = 200;
      const headers = {};
      const mockRes = {
        setHeader: (k, v) => { headers[k] = v; },
        status: (c) => { statusCode = c; return mockRes; },
        json: (data) => {
          const body = JSON.stringify(data);
          res.writeHead(statusCode, { 'Content-Type': 'application/json', ...headers });
          res.end(body);
        },
        end: () => { res.writeHead(statusCode, headers); res.end(); },
      };

      // Clear require cache so file changes are picked up
      delete require.cache[require.resolve(handlerFile)];
      const handler = require(handlerFile);
      await handler(req, mockRes);
    } catch (err) {
      console.error('[API error]', err.message);
      res.writeHead(500, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: err.message }));
    }
    return;
  }

  // === Static files ===
  // Map clean URLs → index.html (mirrors Vercel rewrites)
  let filePath;
  if (pathname === '/' || pathname === '/accueil') {
    filePath = path.join(ROOT, 'accueil', 'index.html');
  } else if (/^\/propriete\/[^/]+\/[a-f0-9]{24}$/.test(pathname)) {
    filePath = path.join(ROOT, 'propriete', 'index.html');
  } else if (/^\/en\/propriete\/[^/]+\/[a-f0-9]{24}$/.test(pathname)) {
    filePath = path.join(ROOT, 'en', 'propriete', 'index.html');
  } else if (pathname === '/propriete' || pathname === '/propriete/') {
    filePath = path.join(ROOT, 'propriete', 'index.html');
  } else {
    // Try exact file first
    const candidate = path.join(ROOT, pathname.slice(1));
    if (fs.existsSync(candidate) && fs.statSync(candidate).isFile()) {
      filePath = candidate;
    } else if (fs.existsSync(candidate + '.html')) {
      filePath = candidate + '.html';
    } else if (fs.existsSync(path.join(candidate, 'index.html'))) {
      filePath = path.join(candidate, 'index.html');
    } else {
      filePath = null;
    }
  }

  if (!filePath || !fs.existsSync(filePath)) {
    res.writeHead(404, { 'Content-Type': 'text/html' });
    res.end('<h1>404 — Page introuvable</h1>');
    return;
  }

  const ext = path.extname(filePath);
  const mime = MIME[ext] || 'application/octet-stream';
  res.writeHead(200, { 'Content-Type': mime });
  fs.createReadStream(filePath).pipe(res);
});

server.listen(PORT, () => {
  console.log(`\n✅  ALPÉON dev server lancé`);
  console.log(`   → http://localhost:${PORT}/reserver`);
  console.log(`   → http://localhost:${PORT}/accueil`);
  console.log(`   → http://localhost:${PORT}/api/properties\n`);
});
