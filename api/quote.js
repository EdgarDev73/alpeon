/**
 * POST /api/quote
 * Body: { listingId, checkIn, checkOut, guests }
 * Returns real per-night prices from Guesty nightlyRates.
 */
const { getNightlyRates, getListing } = require('./_lib/guesty');

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const { listingId, checkIn, checkOut } = req.body || {};
  if (!listingId || !checkIn || !checkOut) {
    return res.status(400).json({ error: 'Missing listingId, checkIn or checkOut' });
  }

  const nights = Math.round((new Date(checkOut) - new Date(checkIn)) / 86_400_000);
  if (nights < 1) return res.status(400).json({ error: 'Invalid date range' });

  try {
    // 1. Get real per-night prices from Guesty
    const [nightlyRates, listing] = await Promise.all([
      getNightlyRates(listingId, checkIn, checkOut),
      getListing(listingId),
    ]);

    const prices     = listing.prices || {};
    const cleaningFee = prices.cleaningFee || 0;
    const currency    = prices.currency || 'EUR';

    const TAX_RATE = 0.05; // 5% taxe de séjour

    if (nightlyRates && Object.keys(nightlyRates).length > 0) {
      const accommodation = Math.round(Object.values(nightlyRates).reduce((s, p) => s + Number(p), 0) * 100) / 100;
      const subtotal      = Math.round((accommodation + cleaningFee) * 100) / 100;
      const taxAmount     = Math.round(subtotal * TAX_RATE * 100) / 100;
      const totalPrice    = Math.round((subtotal + taxAmount) * 100) / 100;

      return res.status(200).json({
        totalPrice,
        quoteId: null,
        breakdown: {
          nights: Object.keys(nightlyRates).length,
          nightlyRates,
          accommodation,
          cleaningFee,
          taxRate: TAX_RATE,
          taxAmount,
          subtotal,
          currency,
        },
      });
    }

    // Fallback: basePrice × nights × factor
    console.warn('[quote] nightlyRates not available — using basePrice fallback');
    const basePrice     = prices.basePrice || 0;
    const weeklyFactor  = prices.weeklyPriceFactor  || 1;
    const monthlyFactor = prices.monthlyPriceFactor || 1;
    const factor        = nights >= 28 ? monthlyFactor : nights >= 7 ? weeklyFactor : 1;
    const accommodation = Math.round(basePrice * nights * factor * 100) / 100;
    const subtotal      = Math.round((accommodation + cleaningFee) * 100) / 100;
    const taxAmount     = Math.round(subtotal * TAX_RATE * 100) / 100;
    const totalPrice    = Math.round((subtotal + taxAmount) * 100) / 100;

    return res.status(200).json({
      totalPrice,
      quoteId: null,
      fallback: true,
      breakdown: { nights, basePrice, accommodation, cleaningFee, taxRate: TAX_RATE, taxAmount, subtotal, factor, currency },
    });

  } catch (err) {
    console.error('[quote]', err.message);
    return res.status(503).json({ error: 'Pricing temporarily unavailable. Please try again.' });
  }
};
