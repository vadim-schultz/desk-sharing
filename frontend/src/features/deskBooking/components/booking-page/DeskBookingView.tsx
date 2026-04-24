import { Box, Stack } from '@chakra-ui/react';

import type { DeskDto, RoomDto } from '../../types';

import DeskBookingDatePicker from './DeskBookingDatePicker';
import DeskBookingHeader from './DeskBookingHeader';
import DeskBookingQueryStatus from './DeskBookingQueryStatus';
import DeskBookingSameDayNote from './DeskBookingSameDayNote';
import DeskRoomsAccordion from './rooms/DeskRoomsAccordion';

export interface DeskBookingViewProps {
  minDate: string;
  maxDate: string;
  effectiveDate: string;
  onDateChange: (isoDate: string) => void;
  timezone: string;
  showSameDayCutoffNote: boolean;
  loading: boolean;
  isError: boolean;
  error: unknown;
  rooms: RoomDto[] | null;
  bookingDate: string;
  sameDayBookingClosed: boolean;
  displayNames: Record<string, string>;
  onDisplayNameChange: (deskId: string, value: string) => void;
  onEnsureName: (deskId: string) => string;
  onBook: (desk: DeskDto) => Promise<void>;
  onCheckIn: (desk: DeskDto) => Promise<void>;
}

export default function DeskBookingView({
  minDate,
  maxDate,
  effectiveDate,
  onDateChange,
  timezone,
  showSameDayCutoffNote,
  loading,
  isError,
  error,
  rooms,
  bookingDate,
  sameDayBookingClosed,
  displayNames,
  onDisplayNameChange,
  onEnsureName,
  onBook,
  onCheckIn,
}: DeskBookingViewProps) {
  return (
    <Box maxW="960px" mx="auto" p={{ base: 4, md: 8 }}>
      <Stack gap={6}>
        <DeskBookingHeader />

        <DeskBookingDatePicker
          minDate={minDate}
          maxDate={maxDate}
          value={effectiveDate}
          onChange={onDateChange}
          timezone={timezone}
        />

        <DeskBookingSameDayNote
          show={showSameDayCutoffNote}
          timezone={timezone}
        />

        <DeskBookingQueryStatus loading={loading} isError={isError} error={error} />

        {rooms !== null ? (
          <DeskRoomsAccordion
            rooms={rooms}
            bookingDate={bookingDate}
            minDate={minDate}
            maxDate={maxDate}
            sameDayBookingClosed={sameDayBookingClosed}
            displayNames={displayNames}
            onDisplayNameChange={onDisplayNameChange}
            onEnsureName={onEnsureName}
            onBook={onBook}
            onCheckIn={onCheckIn}
          />
        ) : null}
      </Stack>
    </Box>
  );
}
