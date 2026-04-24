import { Accordion } from '@chakra-ui/react';

import type { DeskDto, RoomDto } from '../../../types';

import DeskRoomAccordionItem from './DeskRoomAccordionItem';

interface DeskRoomsAccordionProps {
  rooms: RoomDto[];
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

export default function DeskRoomsAccordion({
  rooms,
  bookingDate,
  minDate,
  maxDate,
  sameDayBookingClosed,
  displayNames,
  onDisplayNameChange,
  onEnsureName,
  onBook,
  onCheckIn,
}: DeskRoomsAccordionProps) {
  return (
    <Accordion.Root multiple defaultValue={[]}>
      {rooms.map((room) => (
        <DeskRoomAccordionItem
          key={room.id}
          room={room}
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
      ))}
    </Accordion.Root>
  );
}
