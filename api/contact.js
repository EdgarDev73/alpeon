const nodemailer = require('nodemailer');

module.exports = async (req, res) => {
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const { firstName, lastName, email, phone, message, propertyName } = req.body || {};

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
    return res.status(500).json({ error: 'Send failed. Please try again.' });
  }
};
