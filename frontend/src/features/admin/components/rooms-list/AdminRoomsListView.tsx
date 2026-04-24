import { Box, Stack } from '@chakra-ui/react';

import type { AdminRoomDto } from '../../types';

import AddRoomDialog from './AddRoomDialog';
import RoomsListEmptyHint from './RoomsListEmptyHint';
import RoomsListQueryStatus from './RoomsListQueryStatus';
import RoomsListToolbar from './RoomsListToolbar';
import RoomsListTable from './table/RoomsListTable';

export interface AdminRoomsListViewProps {
  isPending: boolean;
  isError: boolean;
  error: unknown;
  rooms: AdminRoomDto[] | undefined;
  onRequestCreateRoom: () => void;
  onDeleteRoom: (roomId: string) => void;
  createOpen: boolean;
  onCreateOpenChange: (open: boolean) => void;
  roomNumber: string;
  onRoomNumberChange: (value: string) => void;
  description: string;
  onDescriptionChange: (value: string) => void;
  onConfirmCreateRoom: () => void;
  createPending: boolean;
}

export default function AdminRoomsListView({
  isPending,
  isError,
  error,
  rooms,
  onRequestCreateRoom,
  onDeleteRoom,
  createOpen,
  onCreateOpenChange,
  roomNumber,
  onRoomNumberChange,
  description,
  onDescriptionChange,
  onConfirmCreateRoom,
  createPending,
}: AdminRoomsListViewProps) {
  const showEmptyHint = rooms !== undefined && rooms.length === 0;

  return (
    <Box maxW="960px" mx="auto" py={8} px={4}>
      <Stack gap={6}>
        <RoomsListToolbar onRequestCreateRoom={onRequestCreateRoom} />

        <RoomsListQueryStatus
          isPending={isPending}
          isError={isError}
          error={error}
        />

        {rooms !== undefined ? (
          <RoomsListTable rooms={rooms} onDeleteRoom={onDeleteRoom} />
        ) : null}

        {showEmptyHint ? <RoomsListEmptyHint /> : null}
      </Stack>

      <AddRoomDialog
        open={createOpen}
        onOpenChange={onCreateOpenChange}
        roomNumber={roomNumber}
        onRoomNumberChange={onRoomNumberChange}
        description={description}
        onDescriptionChange={onDescriptionChange}
        onConfirmCreate={onConfirmCreateRoom}
        createPending={createPending}
      />
    </Box>
  );
}
