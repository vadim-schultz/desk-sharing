import { Accordion, Stack } from '@chakra-ui/react';

import { DeskRow } from '../../DeskRow';
import type { DeskDto, RoomDto } from '../../../types';

interface DeskRoomAccordionContentProps {
  room: RoomDto;
  bookingDate: string;
  minDate: string;
  maxDate: string;
  sameDayBookingClosed: boolean;
  displayNames: Record<string, string>;
  onDisplayNameChange: (deskId: string, value: string) => void;
  onEnsureName: (deskId: string) => string;
  onBook: (desk: DeskDto) => Promise<void>;
  onCheckIn: (desk: DeskDto) => Promise<void>;
}

export default function DeskRoomAccordionContent({
  room,
  bookingDate,
  minDate,
  maxDate,
  sameDayBookingClosed,
  displayNames,
  onDisplayNameChange,
  onEnsureName,
  onBook,
  onCheckIn,
}: DeskRoomAccordionContentProps) {
  return (
    <Accordion.ItemContent>
      <Stack gap={4} pt={2}>
        {room.desks.map((desk) => (
          <DeskRow
            key={desk.id}
            desk={desk}
            bookingDate={bookingDate}
            minDate={minDate}
            maxDate={maxDate}
            sameDayBookingClosed={sameDayBookingClosed}
            displayName={displayNames[desk.id] ?? ''}
            onDisplayNameChange={(v) => onDisplayNameChange(desk.id, v)}
            onEnsureName={() => onEnsureName(desk.id)}
            onBook={() => onBook(desk)}
            onCheckIn={() => onCheckIn(desk)}
          />
        ))}
      </Stack>
    </Accordion.ItemContent>
  );
}
