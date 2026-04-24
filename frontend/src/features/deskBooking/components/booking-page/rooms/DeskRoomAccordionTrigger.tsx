import { Accordion, HStack, Stack, Text } from '@chakra-ui/react';

import type { RoomDto } from '../../../types';

import DeskRoomStatusStrip from './DeskRoomStatusStrip';

interface DeskRoomAccordionTriggerProps {
  room: RoomDto;
}

export default function DeskRoomAccordionTrigger({ room }: DeskRoomAccordionTriggerProps) {
  return (
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
        <HStack gap={2} flexWrap="wrap" flexShrink={0} align="center">
          <DeskRoomStatusStrip desks={room.desks} />
          <Accordion.ItemIndicator />
        </HStack>
      </HStack>
    </Accordion.ItemTrigger>
  );
}
