import type { DeskDayStatus, DeskDto } from '../types';

/** Order for showing non-zero desk counts in room headers. */
export const DESK_STATUS_DISPLAY_ORDER: DeskDayStatus[] = [
  'bookable',
  'pending',
  'booked',
  'unavailable',
];

export function countDeskStatuses(
  desks: DeskDto[],
): Record<DeskDayStatus, number> {
  const counts: Record<DeskDayStatus, number> = {
    bookable: 0,
    pending: 0,
    booked: 0,
    unavailable: 0,
  };
  for (const d of desks) {
    counts[d.status]++;
  }
  return counts;
}

export function statusPalette(
  status: DeskDto['status'],
): 'green' | 'yellow' | 'red' | 'gray' {
  switch (status) {
    case 'bookable':
      return 'green';
    case 'pending':
      return 'yellow';
    case 'booked':
      return 'red';
    default:
      return 'gray';
  }
}

export function statusLabel(status: DeskDto['status']): string {
  switch (status) {
    case 'bookable':
      return 'Bookable';
    case 'pending':
      return 'Pending check-in';
    case 'booked':
      return 'Booked';
    default:
      return 'Unavailable';
  }
}
