const nodemailer = require('nodemailer');

module.exports = async (req, res) => {
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const body = req.body || {};

  // ── Lead estimateur ───────────────────────────────────────────────────────
  if (body.type === 'lead') {
    const ZAPIER_URL = process.env.ZAPIER_ESTIMATEUR_WEBHOOK;
    if (ZAPIER_URL) {
      fetch(ZAPIER_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      }).catch(e => console.warn('[zapier-lead]', e.message));
    }
    return res.status(200).json({ ok: true });
  }

  // ── Callback request (popup Réserver / Book) ──────────────────────────────
  if (body.type === 'callback') {
    const name  = (body.name  || '').trim();
    const phone = (body.phone || '').trim();
    const dest  = (body.destination || '').trim();
    const lang  = body.lang === 'en' ? 'en' : 'fr';
    if (!name || !phone) return res.status(400).json({ error: 'Nom et téléphone requis.' });
    console.log(`[callback] ${name} · ${phone} · ${dest || '—'} (${lang})`);

    const { EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASS } = process.env;
    if (!EMAIL_HOST || !EMAIL_USER || !EMAIL_PASS) return res.status(200).json({ ok: true, dev: true });

    const transporter = nodemailer.createTransport({
      host: EMAIL_HOST, port: parseInt(EMAIL_PORT || '465'),
      secure: parseInt(EMAIL_PORT || '465') === 465,
      auth: { user: EMAIL_USER, pass: EMAIL_PASS },
    });
    const destLabel = lang === 'en' ? 'Destination' : 'Destination';
    const subject = lang === 'en'
      ? `Stay enquiry — ${name}${dest ? ' · ' + dest : ''} · ${phone}`
      : `Demande de séjour — ${name}${dest ? ' · ' + dest : ''} · ${phone}`;
    const html = `<div style="font-family:Arial,sans-serif;max-width:560px;margin:0 auto;color:#111">
      <div style="background:#2C3D30;padding:20px 28px"><p style="margin:0;font-size:11px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:#E8CBA0">ALPÉON — ${lang === 'en' ? 'Stay Enquiry' : 'Demande de séjour'}</p></div>
      <div style="padding:28px"><table style="width:100%;border-collapse:collapse;font-size:14px">
        <tr><td style="padding:10px 0;color:#6b7280;width:140px">${lang === 'en' ? 'Name' : 'Prénom'}</td><td style="padding:10px 0;font-weight:600;color:#2C3D30">${name}</td></tr>
        <tr style="border-top:1px solid #f0ece6"><td style="padding:10px 0;color:#6b7280">${lang === 'en' ? 'Phone' : 'Téléphone'}</td><td style="padding:10px 0;font-weight:600;color:#2C3D30"><a href="tel:${phone}" style="color:#2C3D30;text-decoration:none">${phone}</a></td></tr>
        ${dest ? `<tr style="border-top:1px solid #f0ece6"><td style="padding:10px 0;color:#6b7280">${destLabel}</td><td style="padding:10px 0;font-weight:600;color:#2C3D30">${dest}</td></tr>` : ''}
        <tr style="border-top:1px solid #f0ece6"><td style="padding:10px 0;color:#6b7280">Source</td><td style="padding:10px 0;color:#2C3D30">Page ${lang === 'en' ? 'Book' : 'Réserver'} — popup</td></tr>
      </table></div></div>`;
    // Zapier webhook (parallel, non-blocking)
    const ZAPIER_URL = process.env.ZAPIER_CALLBACK_WEBHOOK;
    fetch(ZAPIER_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, phone, destination: dest || '—', lang, source: 'popup-reserver' }),
    }).catch(e => console.warn('[zapier]', e.message));

    try {
      await transporter.sendMail({ from: `ALPÉON <${EMAIL_USER}>`, to: 'reservations@alpeon.fr', subject, html, text: `${name}\n${phone}${dest ? '\n' + dest : ''}` });
    } catch (e) { console.error('[callback] SMTP:', e.message); }
    return res.status(200).json({ ok: true });
  }

  // ── Standard contact form ─────────────────────────────────────────────────
  // Accept both EN field names (firstName/lastName) and FR field names (prenom/nom/tel/station/type)
  const firstName   = body.firstName  || body.prenom || '';
  const lastName    = body.lastName   || body.nom    || '';
  const email       = body.email      || '';
  const phone       = body.phone      || body.tel    || '';
  const message     = body.message    || '';
  const propertyName = body.propertyName || [body.station, body.formType].filter(Boolean).join(' — ') || '';

  if (!firstName || !lastName || !email || !message) {
    return res.status(400).json({ error: 'Champs obligatoires manquants.' });
  }

  const { EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASS } = process.env;
  const TO = 'reservations@alpeon.fr';

  if (!EMAIL_HOST || !EMAIL_USER || !EMAIL_PASS) {
    console.warn('[contact] SMTP non configuré');
    return res.status(200).json({ ok: true, dev: true });
  }

  const transporter = nodemailer.createTransport({
    host: EMAIL_HOST,
    port: parseInt(EMAIL_PORT || '587'),
    secure: parseInt(EMAIL_PORT || '587') === 465,
    auth: { user: EMAIL_USER, pass: EMAIL_PASS },
  });

  const html = `
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;color:#111">
      <div style="background:#2C3D30;padding:20px 28px">
        <p style="margin:0;font-size:11px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:#E8CBA0">ALPÉON — New Enquiry</p>
      </div>
      <div style="padding:28px">
        <h2 style="margin:0 0 4px;font-size:18px;font-weight:500;color:#2C3D30">${firstName} ${lastName}</h2>
        <p style="margin:0 0 20px;font-size:13px;color:#6b7280">
          <a href="mailto:${email}" style="color:#2C3D30">${email}</a>${phone ? ` &nbsp;·&nbsp; ${phone}` : ''}
        </p>
        ${propertyName ? `<p style="background:#f5f3ef;border-left:3px solid #E8CBA0;padding:10px 14px;font-size:13px;margin:0 0 20px;color:#2C3D30"><strong>Property:</strong> ${propertyName}</p>` : ''}
        <div style="background:#f5f3ef;border-radius:6px;padding:16px 20px;font-size:14px;line-height:1.7;white-space:pre-wrap">${message}</div>
        <hr style="border:none;border-top:1px solid #eae6df;margin:24px 0">
        <p style="font-size:11px;color:#9ca3af">Sent via ALPÉON contact form.</p>
      </div>
    </div>`;

  // Zapier webhook (parallel, non-blocking)
  const ZAPIER_URL = process.env.ZAPIER_CALLBACK_WEBHOOK;
  if (ZAPIER_URL) {
    const source = body.source || 'propriete-contact';
    const lang   = body.lang   || 'fr';
    fetch(ZAPIER_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name:        `${firstName} ${lastName}`.trim(),
        phone:       phone || '—',
        source,
        destination: propertyName || '—',
        lang,
      }),
    }).catch(e => console.warn('[zapier-contact]', e.message));
  }

  try {
    await transporter.sendMail({
      from: `ALPÉON <${EMAIL_USER}>`,
      to: TO,
      replyTo: email,
      subject: `Enquiry — ${propertyName || 'ALPÉON Property'} — ${firstName} ${lastName}`,
      html,
      text: `${firstName} ${lastName} <${email}>${phone ? ` · ${phone}` : ''}\nProperty: ${propertyName || '—'}\n\n${message}`,
    });
    return res.status(200).json({ ok: true });
  } catch (err) {
    console.error('[contact] SMTP error:', err.message);
    // Never return 500 — email failed silently, the lead is logged server-side
    return res.status(200).json({ ok: true, _error: 'smtp_failed' });
  }
};
