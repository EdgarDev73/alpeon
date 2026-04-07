const { guestyFetch } = require('./_lib/guesty');
const nodemailer = require('nodemailer');

// ── Helpers ────────────────────────────────────────────────────────────────
const fmtShort = d => new Date(d).toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' });
const fmtMoney = n => Number(n).toLocaleString('en-GB', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
const countNights = (i, o) => Math.round((new Date(o) - new Date(i)) / 86400000);

// ── Email ──────────────────────────────────────────────────────────────────
async function sendConfirmationEmail({ guest, reservation, listing, quote, checkIn, checkOut }) {
  const { EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASS, EMAIL_FROM } = process.env;
  if (!EMAIL_HOST || !EMAIL_USER || !EMAIL_PASS) {
    console.warn('[email] SMTP non configuré — email non envoyé');
    return;
  }

  const transporter = nodemailer.createTransport({
    host: EMAIL_HOST,
    port: parseInt(EMAIL_PORT || '587'),
    secure: parseInt(EMAIL_PORT || '587') === 465,
    auth: { user: EMAIL_USER, pass: EMAIL_PASS },
  });

  // ── Data from Guesty ──
  const confirmationCode = reservation.confirmationCode || reservation._id;
  const n = countNights(checkIn, checkOut);

  // Listing
  const listingName    = listing?.title || listing?.nickname || 'Propriété ALPÉON';
  const listingAddress = listing?.address?.full || '';
  const listingCity    = listing?.address?.city || '';
  const photoUrl       = getPhotoUrl(listing);

  // Money from quote
  const money    = quote?.rates?.ratePlans?.[0]?.ratePlan?.money || {};
  const items    = money.invoiceItems || [];
  const accom    = money.fareAccommodationAdjusted || money.fareAccommodation || 0;
  const cleaning = money.fareCleaning || 0;
  const taxes    = money.totalTaxes || 0;
  const total    = (money.subTotalPrice || (accom + cleaning)) + taxes;
  const symbol   = money.currency === 'EUR' ? '€' : (money.currency || 'EUR');

  // ETA / ETD from reservation
  const etaTime = reservation.eta ? new Date(reservation.eta).toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' }) : '4:00 PM';
  const etdTime = reservation.etd ? new Date(reservation.etd).toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' }) : '10:00 AM';
  const guestsCount = reservation.guestsCount || 2;

  // Cancellation policy
  const policyMap = {
    flexible:        'Flexible — full refund up to 24 hours before check-in.',
    moderate:        'Moderate — full refund up to 5 days before check-in.',
    strict:          'Strict — 50% refund for cancellations made at least 7 days before check-in.',
    super_strict_30: 'Very strict — 50% refund for cancellations made at least 30 days before check-in.',
    super_strict_60: 'Very strict — 50% refund for cancellations made at least 60 days before check-in.',
  };
  const policy      = quote?.rates?.ratePlans?.[0]?.ratePlan?.cancellationPolicy || '';
  const policyLabel = policyMap[policy] || '';

  // Invoice rows
  const invoiceRows = items.length
    ? items.map(item => `
        <tr>
          <td style="padding:11px 0;border-bottom:1px solid #EBEBEB;color:#444;font-size:13.5px;font-family:Arial,Helvetica,sans-serif">${item.title}</td>
          <td style="padding:11px 0;border-bottom:1px solid #EBEBEB;text-align:right;color:#444;font-size:13.5px;font-family:Arial,Helvetica,sans-serif;white-space:nowrap">${fmtMoney(item.amount)} ${symbol}</td>
        </tr>`).join('')
    : `<tr>
        <td style="padding:11px 0;border-bottom:1px solid #EBEBEB;color:#444;font-size:13.5px;font-family:Arial,Helvetica,sans-serif">Accommodation · ${n} night${n > 1 ? 's' : ''}</td>
        <td style="padding:11px 0;border-bottom:1px solid #EBEBEB;text-align:right;color:#444;font-size:13.5px;font-family:Arial,Helvetica,sans-serif;white-space:nowrap">${fmtMoney(accom)} ${symbol}</td>
      </tr>
      ${cleaning ? `<tr>
        <td style="padding:11px 0;border-bottom:1px solid #EBEBEB;color:#444;font-size:13.5px;font-family:Arial,Helvetica,sans-serif">Cleaning fee</td>
        <td style="padding:11px 0;border-bottom:1px solid #EBEBEB;text-align:right;color:#444;font-size:13.5px;font-family:Arial,Helvetica,sans-serif;white-space:nowrap">${fmtMoney(cleaning)} ${symbol}</td>
      </tr>` : ''}
      ${taxes ? `<tr>
        <td style="padding:11px 0;border-bottom:1px solid #EBEBEB;color:#444;font-size:13.5px;font-family:Arial,Helvetica,sans-serif">Tourist tax</td>
        <td style="padding:11px 0;border-bottom:1px solid #EBEBEB;text-align:right;color:#444;font-size:13.5px;font-family:Arial,Helvetica,sans-serif;white-space:nowrap">${fmtMoney(taxes)} ${symbol}</td>
      </tr>` : ''}`;

  const html = `<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<title>Booking Confirmation — ALPÉON</title>
</head>
<body style="margin:0;padding:0;background:#EDEAE5;-webkit-text-size-adjust:100%">

<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#EDEAE5;padding:48px 16px">
<tr><td align="center">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;background:#ffffff;border-radius:4px;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,.08)">

  <!-- HEADER -->
  <tr>
    <td style="background:#2C3D30;padding:20px 48px;text-align:center">
      <img src="https://alpeon.fr/assets/logo/logo-main-gold.svg" alt="ALPÉON" height="36" style="height:36px;display:block;margin:0 auto;border:0">
    </td>
  </tr>

  <!-- CONFIRMATION -->
  <tr>
    <td style="padding:40px 48px 32px;border-bottom:1px solid #EBEBEB">
      <p style="font-family:Arial,Helvetica,sans-serif;font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:#2C3D30;font-weight:700;margin:0 0 10px">Booking Confirmed</p>
      <h1 style="font-family:Georgia,'Times New Roman',serif;font-size:24px;font-weight:400;font-style:italic;color:#111111;margin:0 0 6px;line-height:1.2">${listingName}</h1>
      ${listingAddress ? `<p style="font-family:Arial,Helvetica,sans-serif;font-size:13px;color:#888;margin:0 0 20px">${listingAddress}</p>` : ''}
      <table role="presentation" cellpadding="0" cellspacing="0">
        <tr>
          <td style="background:#2C3D30;padding:7px 16px;border-radius:2px">
            <span style="font-family:Arial,Helvetica,sans-serif;font-size:11px;color:#E8CBA0;letter-spacing:.14em;text-transform:uppercase;font-weight:600">Ref. ${confirmationCode}</span>
          </td>
        </tr>
      </table>
    </td>
  </tr>

  <!-- DATES -->
  <tr>
    <td style="padding:0;border-bottom:1px solid #EBEBEB">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
        <tr>
          <td width="50%" style="padding:28px 32px 28px 48px;border-right:1px solid #EBEBEB;vertical-align:top">
            <p style="font-family:Arial,Helvetica,sans-serif;font-size:10px;letter-spacing:.15em;text-transform:uppercase;color:#999;margin:0 0 8px">Check-in</p>
            <p style="font-family:Arial,Helvetica,sans-serif;font-size:15px;font-weight:700;color:#111;margin:0 0 4px">${fmtShort(checkIn)}</p>
            <p style="font-family:Arial,Helvetica,sans-serif;font-size:13px;color:#666;margin:0">From ${etaTime}</p>
          </td>
          <td width="50%" style="padding:28px 48px 28px 32px;vertical-align:top">
            <p style="font-family:Arial,Helvetica,sans-serif;font-size:10px;letter-spacing:.15em;text-transform:uppercase;color:#999;margin:0 0 8px">Check-out</p>
            <p style="font-family:Arial,Helvetica,sans-serif;font-size:15px;font-weight:700;color:#111;margin:0 0 4px">${fmtShort(checkOut)}</p>
            <p style="font-family:Arial,Helvetica,sans-serif;font-size:13px;color:#666;margin:0">By ${etdTime}</p>
          </td>
        </tr>
        <tr>
          <td colspan="2" style="padding:14px 48px;background:#F7F5F2;border-top:1px solid #EBEBEB">
            <p style="font-family:Arial,Helvetica,sans-serif;font-size:13px;color:#2C3D30;font-weight:600;margin:0;text-align:center">${n} night${n > 1 ? 's' : ''} &nbsp;·&nbsp; ${guestsCount} guest${guestsCount > 1 ? 's' : ''}</p>
          </td>
        </tr>
      </table>
    </td>
  </tr>

  <!-- PRICE BREAKDOWN -->
  <tr>
    <td style="padding:28px 48px 32px;border-bottom:1px solid #EBEBEB">
      <p style="font-family:Arial,Helvetica,sans-serif;font-size:11px;letter-spacing:.15em;text-transform:uppercase;color:#999;font-weight:600;margin:0 0 16px">Price Breakdown</p>
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
        ${invoiceRows}
        <tr>
          <td style="padding:16px 0 0;font-family:Arial,Helvetica,sans-serif;font-size:15px;font-weight:700;color:#111">Total (incl. taxes)</td>
          <td style="padding:16px 0 0;text-align:right;font-family:Arial,Helvetica,sans-serif;font-size:15px;font-weight:700;color:#2C3D30;white-space:nowrap">${fmtMoney(total)} ${symbol}</td>
        </tr>
      </table>
    </td>
  </tr>

  <!-- GUEST -->
  <tr>
    <td style="padding:28px 48px 32px;border-bottom:1px solid #EBEBEB">
      <p style="font-family:Arial,Helvetica,sans-serif;font-size:11px;letter-spacing:.15em;text-transform:uppercase;color:#999;font-weight:600;margin:0 0 16px">Guest Details</p>
      <table role="presentation" cellpadding="0" cellspacing="0">
        <tr><td style="padding:4px 0;font-family:Arial,Helvetica,sans-serif;font-size:13.5px;color:#444;width:110px">Name</td><td style="padding:4px 0;font-family:Arial,Helvetica,sans-serif;font-size:13.5px;color:#111;font-weight:600">${guest.firstName} ${guest.lastName}</td></tr>
        <tr><td style="padding:4px 0;font-family:Arial,Helvetica,sans-serif;font-size:13.5px;color:#444">Email</td><td style="padding:4px 0;font-family:Arial,Helvetica,sans-serif;font-size:13.5px;color:#111">${guest.email}</td></tr>
        ${guest.phone ? `<tr><td style="padding:4px 0;font-family:Arial,Helvetica,sans-serif;font-size:13.5px;color:#444">Phone</td><td style="padding:4px 0;font-family:Arial,Helvetica,sans-serif;font-size:13.5px;color:#111">${guest.phone}</td></tr>` : ''}
      </table>
    </td>
  </tr>

  ${policyLabel ? `<!-- CANCELLATION -->
  <tr>
    <td style="padding:24px 48px 28px;border-bottom:1px solid #EBEBEB;background:#FAFAF8">
      <p style="font-family:Arial,Helvetica,sans-serif;font-size:11px;letter-spacing:.15em;text-transform:uppercase;color:#999;font-weight:600;margin:0 0 8px">Cancellation Policy</p>
      <p style="font-family:Arial,Helvetica,sans-serif;font-size:13px;color:#555;margin:0;line-height:1.6">${policyLabel}</p>
    </td>
  </tr>` : ''}

  <!-- MESSAGE -->
  <tr>
    <td style="padding:36px 48px 40px">
      <p style="font-family:Georgia,'Times New Roman',serif;font-size:16px;font-style:italic;color:#2C3D30;margin:0 0 20px">Dear ${guest.firstName},</p>
      <p style="font-family:Arial,Helvetica,sans-serif;font-size:14px;color:#444;line-height:1.75;margin:0 0 14px">Your booking is confirmed. Our team will be in touch ahead of your arrival with access instructions and all practical information you need.</p>
      <p style="font-family:Arial,Helvetica,sans-serif;font-size:14px;color:#444;line-height:1.75;margin:0 0 28px">For any enquiries, please contact us at <a href="mailto:reservations@alpeon.fr" style="color:#2C3D30;font-weight:600;text-decoration:none">reservations@alpeon.fr</a></p>
      <p style="font-family:Arial,Helvetica,sans-serif;font-size:14px;color:#111;margin:0">The ALPÉON Team</p>
    </td>
  </tr>

  <!-- FOOTER -->
  <tr>
    <td style="background:#2C3D30;padding:20px 48px;text-align:center">
      <p style="font-family:Arial,Helvetica,sans-serif;font-size:12px;color:rgba(255,255,255,.45);margin:0 0 6px">ALPÉON — Alpine Property Management</p>
      <p style="font-family:Arial,Helvetica,sans-serif;font-size:11px;color:rgba(255,255,255,.3);margin:0">
        &copy; ${new Date().getFullYear()} ALPÉON &nbsp;·&nbsp;
        <a href="https://alpeon.fr/cgv" style="color:rgba(255,255,255,.4);text-decoration:none">Terms &amp; Conditions</a> &nbsp;·&nbsp;
        <a href="https://alpeon.fr/politique-confidentialite" style="color:rgba(255,255,255,.4);text-decoration:none">Privacy Policy</a>
      </p>
    </td>
  </tr>

</table>
</td></tr>
</table>

</body>
</html>`;

  await transporter.sendMail({
    from: EMAIL_FROM || `ALPÉON <${EMAIL_USER}>`,
    to: guest.email,
    subject: `Booking Confirmed — ${listingName} · ${confirmationCode}`,
    html,
  });
  console.log('[email] Confirmation sent to', guest.email);
}

// ── Main handler ───────────────────────────────────────────────────────────
module.exports = async (req, res) => {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const { listingId, checkIn, checkOut, guests, guest, paymentIntentId } = req.body || {};
  if (!listingId || !checkIn || !checkOut || !guest?.email) {
    return res.status(400).json({ error: 'Champs requis manquants' });
  }

  try {
    // Step 1 — Create quote
    const quote = await guestyFetch('/reservations/quotes', {
      method: 'POST',
      body: {
        listingId,
        checkInDateLocalized: checkIn,
        checkOutDateLocalized: checkOut,
        guestsCount: guests || 2,
      }
    });

    const quoteId = quote._id || quote.id;
    if (!quoteId) throw new Error('Quote ID manquant dans la réponse Guesty');

    // Step 2 — Instant book from quote
    const ratePlanId = quote?.rates?.ratePlans?.[0]?.ratePlan?._id;
    const reservation = await guestyFetch(`/reservations/quotes/${quoteId}/instant`, {
      method: 'POST',
      body: {
        ratePlanId,
        paymentMethod: 'EXTERNAL',
        ccToken: 'EXTERNAL',
        guest: {
          firstName: guest.firstName || '',
          lastName:  guest.lastName  || '',
          email:     guest.email,
          phone:     guest.phone || '',
        },
        ...(paymentIntentId ? { externalPaymentId: paymentIntentId } : {}),
      }
    });

    const confirmationCode = reservation.confirmationCode || reservation._id || reservation.id;

    // Step 3 — Fetch listing details for email
    const listing = await guestyFetch(`/listings/${listingId}`).catch(() => null);

    // Step 4 — Send confirmation email (non-blocking)
    sendConfirmationEmail({ guest, reservation, listing, quote, checkIn, checkOut })
      .catch(e => console.error('[email] Erreur envoi:', e.message));

    res.json({
      reservationId: reservation._id || reservation.id,
      confirmationCode,
      status: reservation.status,
    });

  } catch (e) {
    console.error('[reservations] Erreur:', e.message);
    // Return 502 (upstream failure) instead of 500 so monitoring can distinguish our errors from Guesty's
    res.status(502).json({ error: 'Booking service temporarily unavailable. Please try again or contact us.' });
  }
};
