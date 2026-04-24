import { Button, Heading, HStack } from '@chakra-ui/react';

import type { AdminRoomDto } from '../../../types';
import type { DeskDraft } from '../types';

import RoomDesksTable from './RoomDesksTable';

interface RoomDesksPanelProps {
  room: AdminRoomDto;
  drafts: Record<string, DeskDraft>;
  onDraftChange: (deskId: string, patch: Partial<DeskDraft>) => void;
  onSaveDesk: (deskId: string, body: DeskDraft) => void;
  savePending: boolean;
  onDeleteDesk: (deskId: string) => void;
  onRequestAddDesk: () => void;
}

export default function RoomDesksPanel({
  room,
  drafts,
  onDraftChange,
  onSaveDesk,
  savePending,
  onDeleteDesk,
  onRequestAddDesk,
}: RoomDesksPanelProps) {
  return (
    <>
      <HStack justify="space-between" flexWrap="wrap" gap={3}>
        <Heading size="md">Desks</Heading>
        <Button size="sm" colorPalette="blue" onClick={onRequestAddDesk}>
          Add desk
        </Button>
      </HStack>

      <RoomDesksTable
        desks={room.desks}
        drafts={drafts}
        onDraftChange={onDraftChange}
        onSaveDesk={onSaveDesk}
        savePending={savePending}
        onDeleteDesk={onDeleteDesk}
      />
    </>
  );
}
