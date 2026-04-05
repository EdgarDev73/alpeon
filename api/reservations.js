const { guestyFetch } = require('./_lib/guesty');

module.exports = async (req, res) => {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const { quoteId, listingId, checkIn, checkOut, guests, guest } = req.body || {};
  if (!listingId || !checkIn || !checkOut || !guest?.email) {
    return res.status(400).json({ error: 'Champs requis manquants' });
  }

  const body = {
    listingId,
    checkInDateLocalized: checkIn,
    checkOutDateLocalized: checkOut,
    guestsCount: guests || 2,
    guest: {
      firstName: guest.firstName || '',
      lastName: guest.lastName || '',
      email: guest.email,
      phone: guest.phone || '',
    },
  };
  if (quoteId) body.quoteId = quoteId;

  const reservation = await guestyFetch('/reservations', { method: 'POST', body });
  res.json({
    reservationId: reservation._id || reservation.id || reservation.confirmationCode,
    confirmationCode: reservation.confirmationCode || reservation._id,
    status: reservation.status,
    ...reservation,
  });
};
