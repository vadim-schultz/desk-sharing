import type { RoomsResponse } from '../types';

const base = import.meta.env.VITE_API_BASE ?? '/api';

function url(path: string): string {
  const p = path.startsWith('/') ? path : `/${path}`;
  if (base === '' || base === '/') {
    return p;
  }
  const b = base.endsWith('/') ? base.slice(0, -1) : base;
  return `${b}${p}`;
}

export async function fetchRooms(bookingDate?: string): Promise<RoomsResponse> {
  const qs = bookingDate
    ? `?booking_date=${encodeURIComponent(bookingDate)}`
    : '';
  const res = await fetch(url(`/rooms${qs}`));
  if (!res.ok) {
    throw new Error(await res.text());
  }
  return (await res.json()) as RoomsResponse;
}

export async function createBooking(body: {
  desk_id: string;
  booking_date: string;
  display_name: string;
}): Promise<{ id: string }> {
  const res = await fetch(url('/bookings'), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    throw new Error(await res.text());
  }
  return (await res.json()) as { id: string };
}

export async function checkIn(
  bookingId: string,
  displayName: string,
): Promise<void> {
  const res = await fetch(url(`/bookings/${bookingId}/check-in`), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ display_name: displayName }),
  });
  if (!res.ok) {
    throw new Error(await res.text());
  }
}
