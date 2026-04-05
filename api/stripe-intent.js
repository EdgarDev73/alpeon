module.exports = async (req, res) => {
  const { amount, currency = 'eur', listingId, checkIn, checkOut, guests } = req.body || {};
  if (!amount || amount <= 0) return res.status(400).json({ error: 'Montant invalide' });
  const key = process.env.STRIPE_SECRET_KEY;
  if (!key) return res.status(500).json({ error: 'Stripe non configuré (STRIPE_SECRET_KEY manquant)' });

  const body = new URLSearchParams({
    amount: String(Math.round(Number(amount) * 100)),
    currency,
    // Payment Element requires automatic_payment_methods OR explicit payment_method_types
    'automatic_payment_methods[enabled]': 'true',
    'automatic_payment_methods[allow_redirects]': 'never',
    'metadata[listingId]': listingId || '',
    'metadata[checkIn]': checkIn || '',
    'metadata[checkOut]': checkOut || '',
    'metadata[guests]': String(guests || ''),
  });

  const r = await fetch('https://api.stripe.com/v1/payment_intents', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${key}`, 'Content-Type': 'application/x-www-form-urlencoded' },
    body,
  });
  const data = await r.json();
  if (!r.ok) return res.status(400).json({ error: data.error?.message || 'Erreur Stripe' });
  res.json({ clientSecret: data.client_secret, paymentIntentId: data.id });
};
