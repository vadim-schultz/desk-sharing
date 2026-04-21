import {
  Accordion,
  Box,
  Heading,
  HStack,
  Input,
  Spinner,
  Stack,
  Status,
  Text,
} from '@chakra-ui/react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useEffect, useMemo, useState } from 'react';

import { DeskRow } from '../components/DeskRow';
import { useRoomsQuery } from '../hooks/useRoomsQuery';
import { checkIn, createBooking } from '../services/deskApi';
import {
  addDaysIso,
  isPastSameDayBookingCutoffInTimezone,
  todayIsoInTz,
} from '../utils/date';
import { statusLabel, statusPalette } from '../utils/deskStatus';
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
    Boolean(data) &&
    effectiveDate === minDate &&
    sameDayBookingClosed;

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

  return (
    <Box maxW="960px" mx="auto" p={{ base: 4, md: 8 }}>
      <Stack gap={6}>
        <Heading size="xl">Book a desk</Heading>
        <HStack gap={4} flexWrap="wrap">
          <Text fontWeight="medium">Day</Text>
          <Input
            type="date"
            min={minDate}
            max={maxDate}
            value={effectiveDate}
            onChange={(e) => setViewDate(e.target.value)}
            width="auto"
          />
          <Text color="fg.muted" fontSize="sm">
            Timezone: {tz}
          </Text>
        </HStack>
        {showSameDayCutoffNote && (
          <Text color="fg.muted" fontSize="sm">
            Same-day bookings are not available after 10:00 ({tz}).
          </Text>
        )}

        {loading && (
          <HStack>
            <Spinner size="sm" />
            <Text>Loading…</Text>
          </HStack>
        )}
        {isError && error && (
          <Text color="red.fg" whiteSpace="pre-wrap">
            {error instanceof Error ? error.message : String(error)}
          </Text>
        )}

        {data && !loading && (
          <Accordion.Root multiple defaultValue={[]}>
            {data.rooms.map((room) => (
              <Accordion.Item key={room.id} value={room.id}>
                <Accordion.ItemTrigger>
                  <HStack
                    width="100%"
                    justify="space-between"
                    align="flex-start"
                    gap={3}
                    textAlign="left"
                  >
                    <Stack gap={0} align="flex-start" flex="1" minW={0}>
                      <Text fontWeight="semibold">{room.room_number}</Text>
                      <Text fontSize="sm" color="fg.muted">
                        {room.description}
                      </Text>
                    </Stack>
                    <HStack
                      gap={2}
                      flexWrap="wrap"
                      flexShrink={0}
                      align="center"
                    >
                      <HStack
                        gap={1.5}
                        align="center"
                        aria-label="Status per desk"
                      >
                        {room.desks.map((desk) => (
                          <Status.Root
                            key={desk.id}
                            colorPalette={statusPalette(desk.status)}
                            size="sm"
                            title={`${desk.name}: ${statusLabel(desk.status)}`}
                          >
                            <Status.Indicator />
                          </Status.Root>
                        ))}
                      </HStack>
                      <Accordion.ItemIndicator />
                    </HStack>
                  </HStack>
                </Accordion.ItemTrigger>
                <Accordion.ItemContent>
                  <Stack gap={4} pt={2}>
                    {room.desks.map((desk) => (
                      <DeskRow
                        key={desk.id}
                        desk={desk}
                        bookingDate={data.date}
                        minDate={minDate}
                        maxDate={maxDate}
                        sameDayBookingClosed={sameDayBookingClosed}
                        displayName={names[desk.id] ?? ''}
                        onDisplayNameChange={(v) => setNameFor(desk.id, v)}
                        onEnsureName={() => ensureName(desk.id)}
                        onBook={async () => {
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
                        }}
                        onCheckIn={async () => {
                          const stored = loadStoredBooking(desk.id, data.date);
                          const name = (
                            stored?.displayName ??
                            names[desk.id] ??
                            ''
                          ).trim();
                          if (!desk.booking_id || !name) {
                            return;
                          }
                          await checkInMutation.mutateAsync({
                            bookingId: desk.booking_id,
                            displayName: name,
                          });
                        }}
                      />
                    ))}
                  </Stack>
                </Accordion.ItemContent>
              </Accordion.Item>
            ))}
          </Accordion.Root>
        )}
      </Stack>
    </Box>
  );
}
