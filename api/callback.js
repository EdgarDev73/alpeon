/**
 * POST /api/callback
 * Demande de rappel depuis le popup page Réserver.
 * Champs : name, phone, lang (fr|en)
 */
const nodemailer = require('nodemailer');

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const body = req.body || {};
  const name  = (body.name  || '').trim();
  const phone = (body.phone || '').trim();
  const lang  = body.lang === 'en' ? 'en' : 'fr';

  if (!name || !phone) {
    return res.status(400).json({ error: 'Nom et téléphone requis.' });
  }

  console.log(`[callback] Demande de rappel — ${name} · ${phone} (${lang})`);

  const { EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASS } = process.env;
  const TO = 'reservations@alpeon.fr';

  if (!EMAIL_HOST || !EMAIL_USER || !EMAIL_PASS) {
    console.warn('[callback] SMTP non configuré — lead enregistré localement');
    return res.status(200).json({ ok: true, dev: true });
  }

  const transporter = nodemailer.createTransport({
    host: EMAIL_HOST,
    port: parseInt(EMAIL_PORT || '465'),
    secure: parseInt(EMAIL_PORT || '465') === 465,
    auth: { user: EMAIL_USER, pass: EMAIL_PASS },
  });

  const subject = lang === 'en'
    ? `Callback request — ${name} · ${phone}`
    : `Demande de rappel — ${name} · ${phone}`;

  const html = `
    <div style="font-family:Arial,sans-serif;max-width:560px;margin:0 auto;color:#111">
      <div style="background:#2C3D30;padding:20px 28px">
        <p style="margin:0;font-size:11px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:#E8CBA0">
          ALPÉON — ${lang === 'en' ? 'Callback Request' : 'Demande de rappel'}
        </p>
      </div>
      <div style="padding:28px">
        <table style="width:100%;border-collapse:collapse;font-size:14px">
          <tr>
            <td style="padding:10px 0;color:#6b7280;width:120px">${lang === 'en' ? 'Name' : 'Nom'}</td>
            <td style="padding:10px 0;font-weight:600;color:#2C3D30">${name}</td>
          </tr>
          <tr style="border-top:1px solid #f0ece6">
            <td style="padding:10px 0;color:#6b7280">${lang === 'en' ? 'Phone' : 'Téléphone'}</td>
            <td style="padding:10px 0;font-weight:600;color:#2C3D30">
              <a href="tel:${phone}" style="color:#2C3D30;text-decoration:none">${phone}</a>
            </td>
          </tr>
          <tr style="border-top:1px solid #f0ece6">
            <td style="padding:10px 0;color:#6b7280">Source</td>
            <td style="padding:10px 0;color:#2C3D30">Page ${lang === 'en' ? 'Book' : 'Réserver'} — popup</td>
          </tr>
        </table>
        <hr style="border:none;border-top:1px solid #eae6df;margin:20px 0">
        <p style="font-size:11px;color:#9ca3af">Soumis via popup ALPÉON.fr</p>
      </div>
    </div>`;

  try {
    await transporter.sendMail({
      from: `ALPÉON <${EMAIL_USER}>`,
      to: TO,
      subject,
      html,
      text: `${name}\n${phone}\nSource: page ${lang === 'en' ? 'Book' : 'Réserver'} — popup`,
    });
    return res.status(200).json({ ok: true });
  } catch (err) {
    console.error('[callback] SMTP error:', err.message);
    return res.status(200).json({ ok: true, _error: 'smtp_failed' });
  }
};
