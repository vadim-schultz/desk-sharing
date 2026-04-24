import { Heading, Stack, Text } from '@chakra-ui/react';

import type { AdminRoomDto } from '../../types';

interface RoomDetailSummaryProps {
  room: AdminRoomDto;
}

export default function RoomDetailSummary({ room }: RoomDetailSummaryProps) {
  return (
    <Stack gap={1}>
      <Heading size="lg">{room.room_number}</Heading>
      <Text color="fg.muted">{room.description}</Text>
    </Stack>
  );
}
