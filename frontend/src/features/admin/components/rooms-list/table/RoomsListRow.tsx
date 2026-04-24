import { Button, HStack, Table } from '@chakra-ui/react';
import { Link as RouterLink } from 'react-router-dom';

import type { AdminRoomDto } from '../../../types';

interface RoomsListRowProps {
  room: AdminRoomDto;
  onDelete: () => void;
}

export default function RoomsListRow({ room, onDelete }: RoomsListRowProps) {
  return (
    <Table.Row>
      <Table.Cell fontWeight="medium">{room.room_number}</Table.Cell>
      <Table.Cell color="fg.muted">{room.description}</Table.Cell>
      <Table.Cell textAlign="end">{room.desks.length}</Table.Cell>
      <Table.Cell textAlign="end">
        <HStack gap={2} justify="flex-end">
          <RouterLink to={`/admin/rooms/${room.id}`}>
            <Button size="xs" variant="outline">
              Edit
            </Button>
          </RouterLink>
          <Button size="xs" colorPalette="red" variant="outline" onClick={onDelete}>
            Delete
          </Button>
        </HStack>
      </Table.Cell>
    </Table.Row>
  );
}
