import { Button, HStack, Input, Table } from '@chakra-ui/react';

import type { AdminDeskDto } from '../../../types';
import type { DeskDraft } from '../types';

interface RoomDeskRowProps {
  desk: AdminDeskDto;
  draft: DeskDraft;
  onDraftChange: (deskId: string, patch: Partial<DeskDraft>) => void;
  onSave: () => void;
  savePending: boolean;
  onDelete: () => void;
}

export default function RoomDeskRow({
  desk,
  draft,
  onDraftChange,
  onSave,
  savePending,
  onDelete,
}: RoomDeskRowProps) {
  return (
    <Table.Row>
      <Table.Cell>
        <Input
          size="sm"
          value={draft.name}
          onChange={(e) => onDraftChange(desk.id, { name: e.target.value })}
        />
      </Table.Cell>
      <Table.Cell maxW="100px">
        <Input
          size="sm"
          type="number"
          min={0}
          value={draft.monitor_count}
          onChange={(e) =>
            onDraftChange(desk.id, {
              monitor_count: Number(e.target.value) || 0,
            })
          }
        />
      </Table.Cell>
      <Table.Cell>
        <input
          type="checkbox"
          checked={draft.has_keyboard}
          onChange={(e) =>
            onDraftChange(desk.id, { has_keyboard: e.target.checked })
          }
          aria-label="Keyboard available"
        />
      </Table.Cell>
      <Table.Cell>
        <input
          type="checkbox"
          checked={draft.has_mouse}
          onChange={(e) => onDraftChange(desk.id, { has_mouse: e.target.checked })}
          aria-label="Mouse available"
        />
      </Table.Cell>
      <Table.Cell textAlign="end">
        <HStack gap={2} justify="flex-end">
          <Button
            size="xs"
            colorPalette="blue"
            loading={savePending}
            onClick={onSave}
          >
            Save
          </Button>
          <Button size="xs" colorPalette="red" variant="outline" onClick={onDelete}>
            Delete
          </Button>
        </HStack>
      </Table.Cell>
    </Table.Row>
  );
}
