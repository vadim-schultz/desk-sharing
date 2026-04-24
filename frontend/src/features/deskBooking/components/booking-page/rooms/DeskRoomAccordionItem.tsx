import { Accordion } from '@chakra-ui/react';

import type { DeskDto, RoomDto } from '../../../types';

import DeskRoomAccordionContent from './DeskRoomAccordionContent';
import DeskRoomAccordionTrigger from './DeskRoomAccordionTrigger';

interface DeskRoomAccordionItemProps {
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

export default function DeskRoomAccordionItem({
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
}: DeskRoomAccordionItemProps) {
  return (
    <Accordion.Item value={room.id}>
      <DeskRoomAccordionTrigger room={room} />
      <DeskRoomAccordionContent
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
    </Accordion.Item>
  );
}
