const nodemailer = require('nodemailer');

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const { email } = req.body || {};
  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return res.status(400).json({ error: 'Adresse email invalide.' });
  }

  const dev = !process.env.EMAIL_HOST;
  if (!dev) {
    const transporter = nodemailer.createTransport({
      host: process.env.EMAIL_HOST,
      port: parseInt(process.env.EMAIL_PORT || '465'),
      secure: true,
      auth: { user: process.env.EMAIL_USER, pass: process.env.EMAIL_PASS },
    });
    // Notification interne
    await transporter.sendMail({
      from: process.env.EMAIL_FROM || 'ALPÉON <reservations@alpeon.fr>',
      to: 'reservations@alpeon.fr',
      subject: `Nouvelle inscription newsletter — ${email}`,
      text: `Nouvelle inscription newsletter : ${email}\nDate : ${new Date().toLocaleString('fr-FR')}`,
    });
    // Confirmation à l'inscrit
    await transporter.sendMail({
      from: process.env.EMAIL_FROM || 'ALPÉON <reservations@alpeon.fr>',
      to: email,
      subject: 'Bienvenue chez ALPÉON',
      html: `
        <div style="font-family:Arial,sans-serif;max-width:560px;margin:0 auto;background:#fff">
          <div style="background:#2C3D30;padding:28px 32px">
            <p style="font-family:Georgia,serif;font-style:italic;font-size:22px;color:#E8CBA0;margin:0">ALPÉON</p>
            <p style="font-size:10px;color:rgba(232,203,160,.6);letter-spacing:.2em;text-transform:uppercase;margin:4px 0 0">Alpine Property Management</p>
          </div>
          <div style="padding:32px">
            <h2 style="font-family:Georgia,serif;font-weight:300;color:#2C3D30;margin:0 0 16px">Merci de nous rejoindre</h2>
            <p style="color:#374151;line-height:1.7;font-size:14px">Vous recevrez en avant-première nos nouvelles propriétés, offres de saison et actualités des stations alpines.</p>
            <p style="color:#374151;line-height:1.7;font-size:14px">Pour toute question, contactez-nous à <a href="mailto:reservations@alpeon.fr" style="color:#2C3D30">reservations@alpeon.fr</a>.</p>
          </div>
          <div style="background:#F5F3EF;padding:16px 32px;font-size:11px;color:#9ca3af">© 2026 ALPÉON · Tous droits réservés</div>
        </div>`,
    });
  }

  return res.status(200).json({ ok: true, dev });
};
