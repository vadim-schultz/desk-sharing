const PREFIX = 'desk-sharing:booking:';

export interface StoredBooking {
  bookingId: string;
  displayName: string;
}

export function storageKey(deskId: string, bookingDate: string): string {
  return `${PREFIX}${deskId}:${bookingDate}`;
}

export function loadStoredBooking(
  deskId: string,
  bookingDate: string,
): StoredBooking | null {
  const raw = sessionStorage.getItem(storageKey(deskId, bookingDate));
  if (!raw) {
    return null;
  }
  try {
    const v = JSON.parse(raw) as StoredBooking;
    if (typeof v.bookingId === 'string' && typeof v.displayName === 'string') {
      return v;
    }
  } catch {
    return null;
  }
  return null;
}

export function saveStoredBooking(
  deskId: string,
  bookingDate: string,
  value: StoredBooking,
): void {
  sessionStorage.setItem(
    storageKey(deskId, bookingDate),
    JSON.stringify(value),
  );
}
