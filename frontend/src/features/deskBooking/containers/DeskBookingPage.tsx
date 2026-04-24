import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useEffect, useMemo, useState } from 'react';

import DeskBookingView from '../components/booking-page/DeskBookingView';
import { useRoomsQuery } from '../hooks/useRoomsQuery';
import { checkIn, createBooking } from '../services/deskApi';
import type { DeskDto } from '../types';
import {
  addDaysIso,
  isPastSameDayBookingCutoffInTimezone,
  todayIsoInTz,
} from '../utils/date';
import { randomDisplayName } from '../utils/randomName';
import { loadStoredBooking, saveStoredBooking } from '../utils/storage';

export default function DeskBookingPage() {
  const queryClient = useQueryClient();
  const [viewDate, setViewDate] = useState('');
  const [names, setNames] = useState<Record<string, string>>({});

  const { data, isPending, error, isError } = useRoomsQuery(viewDate);

  useEffect(() => {
    if (data) {
      setViewDate((prev) => prev || data.date);
    }
  }, [data]);

  const tz = data?.timezone ?? 'Europe/Berlin';
  const minDate = useMemo(() => todayIsoInTz(tz), [tz]);
  const maxDate = useMemo(() => addDaysIso(minDate, 5), [minDate]);
  const effectiveDate = viewDate || data?.date || minDate;
  const sameDayBookingClosed = useMemo(
    () => isPastSameDayBookingCutoffInTimezone(tz),
    [tz],
  );
  const showSameDayCutoffNote =
    Boolean(data) && effectiveDate === minDate && sameDayBookingClosed;

  const setNameFor = (deskId: string, value: string) => {
    setNames((prev) => ({ ...prev, [deskId]: value }));
  };

  const ensureName = (deskId: string): string => {
    const existing = names[deskId];
    if (existing && existing.trim()) {
      return existing.trim();
    }
    const generated = randomDisplayName();
    setNameFor(deskId, generated);
    return generated;
  };

  const bookMutation = useMutation({
    mutationFn: createBooking,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ['rooms'] });
    },
  });

  const checkInMutation = useMutation({
    mutationFn: ({
      bookingId,
      displayName: name,
    }: {
      bookingId: string;
      displayName: string;
    }) => checkIn(bookingId, name),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ['rooms'] });
    },
  });

  const loading = isPending;

  const onBook = async (desk: DeskDto) => {
    if (!data) {
      return;
    }
    const name = ensureName(desk.id);
    const created = await bookMutation.mutateAsync({
      desk_id: desk.id,
      booking_date: data.date,
      display_name: name,
    });
    saveStoredBooking(desk.id, data.date, {
      bookingId: created.id,
      displayName: name,
    });
  };

  const onCheckIn = async (desk: DeskDto) => {
    if (!data) {
      return;
    }
    const stored = loadStoredBooking(desk.id, data.date);
    const name = (stored?.displayName ?? names[desk.id] ?? '').trim();
    if (!desk.booking_id || !name) {
      return;
    }
    await checkInMutation.mutateAsync({
      bookingId: desk.booking_id,
      displayName: name,
    });
  };

  return (
    <DeskBookingView
      minDate={minDate}
      maxDate={maxDate}
      effectiveDate={effectiveDate}
      onDateChange={setViewDate}
      timezone={tz}
      showSameDayCutoffNote={showSameDayCutoffNote}
      loading={loading}
      isError={isError}
      error={error}
      rooms={data && !loading ? data.rooms : null}
      bookingDate={data?.date ?? ''}
      sameDayBookingClosed={sameDayBookingClosed}
      displayNames={names}
      onDisplayNameChange={setNameFor}
      onEnsureName={ensureName}
      onBook={onBook}
      onCheckIn={onCheckIn}
    />
  );
}
