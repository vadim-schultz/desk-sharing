import {
  Box,
  Button,
  Heading,
  HStack,
  Input,
  Stack,
  Status,
  Text,
} from '@chakra-ui/react';
import { useEffect, useState } from 'react';

import type { DeskDto } from '../types';
import { statusLabel, statusPalette } from '../utils/deskStatus';
import { randomDisplayName } from '../utils/randomName';
import { loadStoredBooking } from '../utils/storage';

export function DeskRow(props: {
  desk: DeskDto;
  bookingDate: string;
  minDate: string;
  maxDate: string;
  sameDayBookingClosed: boolean;
  displayName: string;
  onDisplayNameChange: (v: string) => void;
  onEnsureName: () => string;
  onBook: () => Promise<void>;
  onCheckIn: () => Promise<void>;
}) {
  const {
    desk,
    bookingDate,
    minDate,
    maxDate,
    sameDayBookingClosed,
    displayName,
    onDisplayNameChange,
    onEnsureName,
    onBook,
    onCheckIn,
  } = props;
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

  const isViewingToday = bookingDate === minDate;
  const canBook =
    desk.bookable &&
    desk.status === 'bookable' &&
    bookingDate >= minDate &&
    bookingDate <= maxDate &&
    !(isViewingToday && sameDayBookingClosed);

  const stored = loadStoredBooking(desk.id, bookingDate);
  const canCheckIn =
    isViewingToday &&
    desk.status === 'pending' &&
    Boolean(desk.booking_id) &&
    Boolean((stored?.displayName ?? displayName).trim());

  return (
    <Box borderWidth="1px" borderRadius="md" borderColor="border" p={4}>
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
          Monitors: {desk.monitor_count} · Keyboard:{' '}
          {desk.has_keyboard ? 'yes' : 'no'} · Mouse:{' '}
          {desk.has_mouse ? 'yes' : 'no'}
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
