export function todayIsoInTz(timezone: string): string {
  const fmt = new Intl.DateTimeFormat('en-CA', {
    timeZone: timezone,
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  });
  const parts = fmt.formatToParts(new Date());
  const y = parts.find((p) => p.type === 'year')?.value;
  const m = parts.find((p) => p.type === 'month')?.value;
  const d = parts.find((p) => p.type === 'day')?.value;
  if (!y || !m || !d) {
    return new Date().toISOString().slice(0, 10);
  }
  return `${y}-${m}-${d}`;
}

export function addDaysIso(isoDate: string, days: number): string {
  const [y, m, d] = isoDate.split('-').map((x) => Number.parseInt(x, 10));
  const dt = new Date(Date.UTC(y!, m! - 1, d!));
  dt.setUTCDate(dt.getUTCDate() + days);
  return dt.toISOString().slice(0, 10);
}

/** Seconds since local midnight in `timezone` for `date` (matches backend 10:00 cutoff semantics). */
function secondsSinceMidnightInTimezone(timezone: string, date: Date): number {
  const fmt = new Intl.DateTimeFormat('en-GB', {
    timeZone: timezone,
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false,
  });
  const parts = fmt.formatToParts(date);
  const h = Number(parts.find((p) => p.type === 'hour')?.value ?? 0);
  const m = Number(parts.find((p) => p.type === 'minute')?.value ?? 0);
  const s = Number(parts.find((p) => p.type === 'second')?.value ?? 0);
  return h * 3600 + m * 60 + s;
}

const SAME_DAY_CUTOFF_SECONDS = 10 * 3600;

/** True if local time in `timezone` is after 10:00 on today's calendar date. */
export function isPastSameDayBookingCutoffInTimezone(
  timezone: string,
): boolean {
  return (
    secondsSinceMidnightInTimezone(timezone, new Date()) >
    SAME_DAY_CUTOFF_SECONDS
  );
}
