import { Table } from '@chakra-ui/react';

import type { AdminDeskDto } from '../../../types';
import type { DeskDraft } from '../types';

import RoomDeskRow from './RoomDeskRow';

interface RoomDesksTableProps {
  desks: AdminDeskDto[];
  drafts: Record<string, DeskDraft>;
  onDraftChange: (deskId: string, patch: Partial<DeskDraft>) => void;
  onSaveDesk: (deskId: string, body: DeskDraft) => void;
  savePending: boolean;
  onDeleteDesk: (deskId: string) => void;
}

export default function RoomDesksTable({
  desks,
  drafts,
  onDraftChange,
  onSaveDesk,
  savePending,
  onDeleteDesk,
}: RoomDesksTableProps) {
  return (
    <Table.Root size="sm" variant="outline">
      <Table.Header>
        <Table.Row>
          <Table.ColumnHeader>Name</Table.ColumnHeader>
          <Table.ColumnHeader>Monitors</Table.ColumnHeader>
          <Table.ColumnHeader>Keyboard</Table.ColumnHeader>
          <Table.ColumnHeader>Mouse</Table.ColumnHeader>
          <Table.ColumnHeader textAlign="end">Actions</Table.ColumnHeader>
        </Table.Row>
      </Table.Header>
      <Table.Body>
        {desks.map((desk) => {
          const draft = drafts[desk.id];
          if (!draft) {
            return null;
          }
          return (
            <RoomDeskRow
              key={desk.id}
              desk={desk}
              draft={draft}
              onDraftChange={onDraftChange}
              onSave={() =>
                onSaveDesk(desk.id, {
                  name: draft.name,
                  monitor_count: draft.monitor_count,
                  has_keyboard: draft.has_keyboard,
                  has_mouse: draft.has_mouse,
                  bookable: draft.bookable,
                })
              }
              savePending={savePending}
              onDelete={() => {
                if (window.confirm(`Delete desk ${desk.name}?`)) {
                  onDeleteDesk(desk.id);
                }
              }}
            />
          );
        })}
      </Table.Body>
    </Table.Root>
  );
}
