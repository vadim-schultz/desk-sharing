import { Table } from '@chakra-ui/react';

import type { AdminRoomDto } from '../../../types';

import RoomsListRow from './RoomsListRow';

interface RoomsListTableProps {
  rooms: AdminRoomDto[];
  onDeleteRoom: (roomId: string) => void;
}

export default function RoomsListTable({
  rooms,
  onDeleteRoom,
}: RoomsListTableProps) {
  return (
    <Table.Root size="sm" variant="outline">
      <Table.Header>
        <Table.Row>
          <Table.ColumnHeader>Room</Table.ColumnHeader>
          <Table.ColumnHeader>Description</Table.ColumnHeader>
          <Table.ColumnHeader textAlign="end">Desks</Table.ColumnHeader>
          <Table.ColumnHeader textAlign="end">Actions</Table.ColumnHeader>
        </Table.Row>
      </Table.Header>
      <Table.Body>
        {rooms.map((room) => (
          <RoomsListRow
            key={room.id}
            room={room}
            onDelete={() => {
              if (
                window.confirm(
                  `Delete room ${room.room_number} and all its desks?`,
                )
              ) {
                onDeleteRoom(room.id);
              }
            }}
          />
        ))}
      </Table.Body>
    </Table.Root>
  );
}
