const nodemailer = require('nodemailer');

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const { email, source } = req.body || {};
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

    const isPopup = source === 'popup-10pct';

    // Notification interne
    await transporter.sendMail({
      from: process.env.EMAIL_FROM || 'ALPÉON <reservations@alpeon.fr>',
      to: 'reservations@alpeon.fr',
      subject: `Nouvelle inscription newsletter — ${email}`,
      text: `Nouvelle inscription newsletter : ${email}\nSource : ${source || 'footer'}\nDate : ${new Date().toLocaleString('fr-FR')}`,
    });

    // Email de bienvenue à l'inscrit
    await transporter.sendMail({
      from: process.env.EMAIL_FROM || 'ALPÉON <reservations@alpeon.fr>',
      to: email,
      subject: isPopup ? 'Votre code -10% ALPÉON — ALPE10' : 'Bienvenue chez ALPÉON',
      html: `<!DOCTYPE html>
<html lang="fr">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#F5F3EF;font-family:Arial,sans-serif">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#F5F3EF;padding:40px 20px">
  <tr><td align="center">
  <table width="560" cellpadding="0" cellspacing="0" style="max-width:560px;width:100%;background:#ffffff;border-radius:8px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,.08)">

    <!-- Header -->
    <tr>
      <td style="background:#2C3D30;padding:32px 40px;text-align:center">
        <p style="font-family:Georgia,serif;font-style:italic;font-size:26px;color:#E8CBA0;margin:0;letter-spacing:.02em">ALPÉON</p>
        <p style="font-size:9px;color:rgba(232,203,160,.55);letter-spacing:.25em;text-transform:uppercase;margin:6px 0 0">Alpine Property Management</p>
      </td>
    </tr>

    ${isPopup ? `
    <!-- Offer block -->
    <tr>
      <td style="background:#2C3D30;padding:0 40px 32px;text-align:center;border-bottom:1px solid rgba(232,203,160,.15)">
        <p style="font-size:11px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:#E8CBA0;margin:0 0 8px">Offre exclusive</p>
        <p style="font-family:Georgia,serif;font-style:italic;font-size:56px;font-weight:300;color:#E8CBA0;margin:0;line-height:1">-10%</p>
        <p style="font-size:13px;color:rgba(232,203,160,.7);margin:6px 0 0">sur votre premier séjour</p>
      </td>
    </tr>
    ` : ''}

    <!-- Body -->
    <tr>
      <td style="padding:36px 40px">
        <h2 style="font-family:Georgia,serif;font-weight:300;font-style:italic;color:#2C3D30;margin:0 0 16px;font-size:22px">
          ${isPopup ? 'Votre code de réduction vous attend' : 'Bienvenue dans la communauté ALPÉON'}
        </h2>
        <p style="color:#374151;line-height:1.75;font-size:14px;margin:0 0 20px">
          ${isPopup
            ? 'Merci de rejoindre la communauté ALPÉON. Voici votre code exclusif pour profiter de <strong>10% de réduction</strong> sur votre premier séjour dans l\'un de nos chalets et appartements alpins d\'exception.'
            : 'Merci de votre inscription. Vous recevrez en avant-première nos nouvelles propriétés, offres de saison et actualités des stations alpines.'}
        </p>

        ${isPopup ? `
        <!-- Code block -->
        <table width="100%" cellpadding="0" cellspacing="0" style="margin:8px 0 28px">
          <tr>
            <td style="background:#F5F3EF;border:2px dashed #D5CFC4;border-radius:6px;padding:20px;text-align:center">
              <p style="font-size:11px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:#6b7280;margin:0 0 8px">Votre code de réduction</p>
              <p style="font-family:Georgia,serif;font-size:28px;font-weight:400;color:#2C3D30;letter-spacing:.12em;margin:0">ALPE10</p>
              <p style="font-size:11px;color:#9ca3af;margin:8px 0 0">À saisir lors de votre réservation sur alpeon.fr</p>
            </td>
          </tr>
        </table>
        ` : ''}

        <p style="color:#374151;line-height:1.75;font-size:14px;margin:0 0 28px">
          Découvrez notre sélection de propriétés dans les stations alpines les plus prestigieuses&nbsp;: Courchevel, Megève, Val d'Isère, Val Thorens, Méribel et Tignes.
        </p>

        <!-- CTA -->
        <table cellpadding="0" cellspacing="0" style="margin:0 auto">
          <tr>
            <td style="background:#2C3D30;border-radius:5px">
              <a href="https://alpeon.fr/reserver" style="display:block;padding:14px 32px;font-size:12px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#E8CBA0;text-decoration:none">
                Explorer nos propriétés
              </a>
            </td>
          </tr>
        </table>
      </td>
    </tr>

    <!-- Divider -->
    <tr><td style="padding:0 40px"><div style="height:1px;background:#EAE6DF"></div></td></tr>

    <!-- Stations -->
    <tr>
      <td style="padding:24px 40px">
        <p style="font-size:11px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:#9ca3af;margin:0 0 10px;text-align:center">Nos destinations</p>
        <p style="font-size:13px;color:#6b7280;text-align:center;margin:0;line-height:1.8">
          Courchevel · Megève · Val d'Isère<br>Val Thorens · Méribel · Tignes
        </p>
      </td>
    </tr>

    <!-- Footer -->
    <tr>
      <td style="background:#2C3D30;padding:20px 40px;text-align:center">
        <p style="font-size:11px;color:rgba(232,203,160,.4);margin:0 0 6px;letter-spacing:.08em">
          <a href="https://alpeon.fr" style="color:rgba(232,203,160,.6);text-decoration:none">alpeon.fr</a>
          &nbsp;·&nbsp;
          <a href="mailto:reservations@alpeon.fr" style="color:rgba(232,203,160,.6);text-decoration:none">reservations@alpeon.fr</a>
        </p>
        <p style="font-size:10px;color:rgba(232,203,160,.25);margin:0">© 2026 ALPÉON · Tous droits réservés</p>
      </td>
    </tr>

  </table>
  </td></tr>
</table>
</body>
</html>`,
    });
  }

  return res.status(200).json({ ok: true, dev });
};
