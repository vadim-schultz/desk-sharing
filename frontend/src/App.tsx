import {
  Accordion,
  Box,
  Button,
  Heading,
  HStack,
  Input,
  Spinner,
  Stack,
  Status,
  Text,
} from "@chakra-ui/react";
import { useCallback, useEffect, useMemo, useState } from "react";

import type { DeskDto, RoomsResponse } from "./api";
import { checkIn, createBooking, fetchRooms } from "./api";
import { randomDisplayName } from "./randomName";
import { loadStoredBooking, saveStoredBooking } from "./storage";

function todayIsoInTz(timezone: string): string {
  const fmt = new Intl.DateTimeFormat("en-CA", {
    timeZone: timezone,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  });
  const parts = fmt.formatToParts(new Date());
  const y = parts.find((p) => p.type === "year")?.value;
  const m = parts.find((p) => p.type === "month")?.value;
  const d = parts.find((p) => p.type === "day")?.value;
  if (!y || !m || !d) {
    return new Date().toISOString().slice(0, 10);
  }
  return `${y}-${m}-${d}`;
}

function addDaysIso(isoDate: string, days: number): string {
  const [y, m, d] = isoDate.split("-").map((x) => Number.parseInt(x, 10));
  const dt = new Date(Date.UTC(y!, m! - 1, d!));
  dt.setUTCDate(dt.getUTCDate() + days);
  return dt.toISOString().slice(0, 10);
}

function statusPalette(status: DeskDto["status"]): "green" | "yellow" | "red" | "gray" {
  switch (status) {
    case "bookable":
      return "green";
    case "pending":
      return "yellow";
    case "booked":
      return "red";
    default:
      return "gray";
  }
}

function statusLabel(status: DeskDto["status"]): string {
  switch (status) {
    case "bookable":
      return "Bookable";
    case "pending":
      return "Pending check-in";
    case "booked":
      return "Booked";
    default:
      return "Unavailable";
  }
}

export function App(): JSX.Element {
  const [data, setData] = useState<RoomsResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [viewDate, setViewDate] = useState<string>("");
  const [names, setNames] = useState<Record<string, string>>({});

  const refresh = useCallback(async (dateIso: string | undefined) => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetchRooms(dateIso);
      setData(res);
      setViewDate((prev) => prev || res.date);
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void refresh(viewDate || undefined);
  }, [refresh, viewDate]);

  const tz = data?.timezone ?? "Europe/Berlin";
  const minDate = useMemo(() => todayIsoInTz(tz), [tz]);
  const maxDate = useMemo(() => addDaysIso(minDate, 5), [minDate]);

  const effectiveDate = viewDate || data?.date || minDate;

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

  return (
    <Box maxW="960px" mx="auto" p={{ base: 4, md: 8 }}>
      <Stack gap={6}>
        <Heading size="xl">Desk sharing</Heading>
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

        {loading && (
          <HStack>
            <Spinner size="sm" />
            <Text>Loading…</Text>
          </HStack>
        )}
        {error && (
          <Text color="red.fg" whiteSpace="pre-wrap">
            {error}
          </Text>
        )}

        {data && !loading && (
          <Accordion.Root multiple defaultValue={data.rooms.map((r) => r.id)}>
            {data.rooms.map((room) => (
              <Accordion.Item key={room.id} value={room.id}>
                <Accordion.ItemTrigger>
                  <Stack gap={0} align="flex-start" textAlign="left">
                    <Text fontWeight="semibold">{room.room_number}</Text>
                    <Text fontSize="sm" color="fg.muted">
                      {room.description}
                    </Text>
                  </Stack>
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
                        displayName={names[desk.id] ?? ""}
                        onDisplayNameChange={(v) => setNameFor(desk.id, v)}
                        onEnsureName={() => ensureName(desk.id)}
                        onBook={async () => {
                          const name = ensureName(desk.id);
                          const created = await createBooking({
                            desk_id: desk.id,
                            booking_date: data.date,
                            display_name: name,
                          });
                          saveStoredBooking(desk.id, data.date, {
                            bookingId: created.id,
                            displayName: name,
                          });
                          await refresh(viewDate || undefined);
                        }}
                        onCheckIn={async () => {
                          const stored = loadStoredBooking(desk.id, data.date);
                          const name = (stored?.displayName ?? names[desk.id] ?? "").trim();
                          if (!desk.booking_id || !name) {
                            return;
                          }
                          await checkIn(desk.booking_id, name);
                          await refresh(viewDate || undefined);
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

function DeskRow(props: {
  desk: DeskDto;
  bookingDate: string;
  minDate: string;
  maxDate: string;
  displayName: string;
  onDisplayNameChange: (v: string) => void;
  onEnsureName: () => string;
  onBook: () => Promise<void>;
  onCheckIn: () => Promise<void>;
}): JSX.Element {
  const { desk, bookingDate, minDate, maxDate, displayName, onDisplayNameChange, onEnsureName, onBook, onCheckIn } =
    props;
  const [busy, setBusy] = useState(false);
  const palette = statusPalette(desk.status);

  useEffect(() => {
    if (displayName) {
      return;
    }
    const stored = loadStoredBooking(desk.id, bookingDate);
    if (stored?.displayName) {
      onDisplayNameChange(stored.displayName);
      return;
    }
    onDisplayNameChange(randomDisplayName());
    // eslint-disable-next-line react-hooks/exhaustive-deps -- seed once per desk/date
  }, [bookingDate, desk.id]);

  const canBook =
    desk.bookable &&
    desk.status === "bookable" &&
    bookingDate >= minDate &&
    bookingDate <= maxDate;

  const stored = loadStoredBooking(desk.id, bookingDate);
  const canCheckIn =
    desk.status === "pending" &&
    Boolean(desk.booking_id) &&
    Boolean((stored?.displayName ?? displayName).trim());

  return (
    <Box borderWidth="1px" borderRadius="md" p={4}>
      <Stack gap={3}>
        <HStack justify="space-between" flexWrap="wrap" gap={3}>
          <Heading size="md">{desk.name}</Heading>
          <HStack gap={2}>
            <Status.Root colorPalette={palette} size="sm">
              <Status.Indicator />
              <Text fontSize="sm">{statusLabel(desk.status)}</Text>
            </Status.Root>
          </HStack>
        </HStack>
        <Text fontSize="sm" color="fg.muted">
          Monitors: {desk.monitor_count} · Keyboard: {desk.has_keyboard ? "yes" : "no"} · Mouse:{" "}
          {desk.has_mouse ? "yes" : "no"}
        </Text>
        <HStack gap={2} flexWrap="wrap" alignItems="flex-end">
          <Box flex="1" minW="200px">
            <Text fontSize="sm" mb={1}>
              Your name (anonymous)
            </Text>
            <Input
              value={displayName}
              onChange={(e) => onDisplayNameChange(e.target.value)}
              onFocus={() => {
                if (!displayName) {
                  onDisplayNameChange(onEnsureName());
                }
              }}
            />
          </Box>
          <Button
            disabled={!canBook || busy}
            onClick={async () => {
              setBusy(true);
              try {
                await onBook();
              } finally {
                setBusy(false);
              }
            }}
          >
            Book
          </Button>
          <Button
            variant="outline"
            disabled={!canCheckIn || busy}
            onClick={async () => {
              setBusy(true);
              try {
                await onCheckIn();
              } finally {
                setBusy(false);
              }
            }}
          >
            Check in
          </Button>
        </HStack>
      </Stack>
    </Box>
  );
}
