import { Box, Stack } from '@chakra-ui/react';

import type { AdminRoomDto } from '../../types';
import type { DeskDraft } from './types';

import AddDeskDialog from './desks/AddDeskDialog';
import RoomDesksPanel from './desks/RoomDesksPanel';
import RoomDetailBackNav from './RoomDetailBackNav';
import RoomDetailQueryStatus from './RoomDetailQueryStatus';
import RoomDetailSummary from './RoomDetailSummary';

export interface AdminRoomDetailViewProps {
  isPending: boolean;
  isError: boolean;
  error: unknown;
  room: AdminRoomDto | undefined;
  drafts: Record<string, DeskDraft>;
  onDraftChange: (deskId: string, patch: Partial<DeskDraft>) => void;
  onSaveDesk: (deskId: string, body: DeskDraft) => void;
  savePending: boolean;
  onDeleteDesk: (deskId: string) => void;
  onRequestAddDesk: () => void;
  addOpen: boolean;
  onAddOpenChange: (open: boolean) => void;
  newDeskName: string;
  onNewDeskNameChange: (name: string) => void;
  onConfirmAddDesk: () => void;
  addPending: boolean;
}

export default function AdminRoomDetailView({
  isPending,
  isError,
  error,
  room,
  drafts,
  onDraftChange,
  onSaveDesk,
  savePending,
  onDeleteDesk,
  onRequestAddDesk,
  addOpen,
  onAddOpenChange,
  newDeskName,
  onNewDeskNameChange,
  onConfirmAddDesk,
  addPending,
}: AdminRoomDetailViewProps) {
  return (
    <Box maxW="960px" mx="auto" py={8} px={4}>
      <Stack gap={6}>
        <RoomDetailBackNav />

        <RoomDetailQueryStatus
          isPending={isPending}
          isError={isError}
          error={error}
        />

        {room ? (
          <>
            <RoomDetailSummary room={room} />
            <RoomDesksPanel
              room={room}
              drafts={drafts}
              onDraftChange={onDraftChange}
              onSaveDesk={onSaveDesk}
              savePending={savePending}
              onDeleteDesk={onDeleteDesk}
              onRequestAddDesk={onRequestAddDesk}
            />
          </>
        ) : null}
      </Stack>

      <AddDeskDialog
        open={addOpen}
        onOpenChange={onAddOpenChange}
        newDeskName={newDeskName}
        onNewDeskNameChange={onNewDeskNameChange}
        onConfirmAdd={onConfirmAddDesk}
        addPending={addPending}
      />
    </Box>
  );
}
