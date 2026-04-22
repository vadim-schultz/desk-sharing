import {
  Box,
  Button,
  Dialog,
  Heading,
  HStack,
  Input,
  Spinner,
  Stack,
  Table,
  Text,
} from '@chakra-ui/react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useEffect, useState } from 'react';
import { Link as RouterLink, useParams } from 'react-router-dom';

import PasswordModal from '../../auth/components/PasswordModal';
import { useAuth } from '../../auth/context/AuthContext';
import type { AdminDeskDto } from '../types';
import {
  createAdminDesk,
  deleteAdminDesk,
  fetchAdminRoom,
  patchAdminDesk,
} from '../services/adminApi';

type DeskDraft = Pick<
  AdminDeskDto,
  'name' | 'monitor_count' | 'has_keyboard' | 'has_mouse' | 'bookable'
>;

export default function AdminRoomDetailPage() {
  const { roomId } = useParams<{ roomId: string }>();
  const { getToken, isAuthenticated } = useAuth();
  const queryClient = useQueryClient();
  const [pwOpen, setPwOpen] = useState(false);
  const [drafts, setDrafts] = useState<Record<string, DeskDraft>>({});
  const [addOpen, setAddOpen] = useState(false);
  const [newDeskName, setNewDeskName] = useState('');

  const tokenReady = isAuthenticated && !!getToken() && !!roomId;

  const roomQuery = useQuery({
    queryKey: ['admin-room', roomId],
    queryFn: () => fetchAdminRoom(getToken, roomId!),
    enabled: tokenReady,
  });

  useEffect(() => {
    const room = roomQuery.data;
    if (!room) {
      return;
    }
    const next: Record<string, DeskDraft> = {};
    for (const d of room.desks) {
      next[d.id] = {
        name: d.name,
        monitor_count: d.monitor_count,
        has_keyboard: d.has_keyboard,
        has_mouse: d.has_mouse,
        bookable: d.bookable,
      };
    }
    setDrafts(next);
  }, [roomQuery.data]);

  const patchMutation = useMutation({
    mutationFn: ({ deskId, body }: { deskId: string; body: Partial<DeskDraft> }) =>
      patchAdminDesk(getToken, deskId, body),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ['admin-room', roomId] });
      void queryClient.invalidateQueries({ queryKey: ['admin-rooms'] });
    },
  });

  const addMutation = useMutation({
    mutationFn: (name: string) =>
      createAdminDesk(getToken, roomId!, {
        name,
        bookable: true,
        monitor_count: 0,
        has_keyboard: false,
        has_mouse: false,
      }),
    onSuccess: () => {
      setAddOpen(false);
      setNewDeskName('');
      void queryClient.invalidateQueries({ queryKey: ['admin-room', roomId] });
      void queryClient.invalidateQueries({ queryKey: ['admin-rooms'] });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (deskId: string) => deleteAdminDesk(getToken, deskId),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ['admin-room', roomId] });
      void queryClient.invalidateQueries({ queryKey: ['admin-rooms'] });
    },
  });

  if (!tokenReady) {
    return (
      <Box maxW="720px" mx="auto" py={8} px={4}>
        <Stack gap={4}>
          <Heading size="lg">Admin: room</Heading>
          <Text color="fg.muted">Sign in to edit desks.</Text>
          <Button colorPalette="blue" w="fit-content" onClick={() => setPwOpen(true)}>
            Sign in to admin
          </Button>
        </Stack>
        <PasswordModal open={pwOpen} onOpenChange={setPwOpen} />
      </Box>
    );
  }

  const room = roomQuery.data;

  return (
    <Box maxW="960px" mx="auto" py={8} px={4}>
      <Stack gap={6}>
        <RouterLink to="/admin/rooms">
          <Button variant="ghost" alignSelf="flex-start">
            ← Back to rooms
          </Button>
        </RouterLink>

        {roomQuery.isPending ? (
          <HStack>
            <Spinner size="sm" />
            <Text>Loading…</Text>
          </HStack>
        ) : null}
        {roomQuery.isError ? (
          <Text color="red.fg" whiteSpace="pre-wrap">
            {roomQuery.error instanceof Error
              ? roomQuery.error.message
              : String(roomQuery.error)}
          </Text>
        ) : null}

        {room ? (
          <>
            <Stack gap={1}>
              <Heading size="lg">{room.room_number}</Heading>
              <Text color="fg.muted">{room.description}</Text>
            </Stack>

            <HStack justify="space-between" flexWrap="wrap" gap={3}>
              <Heading size="md">Desks</Heading>
              <Button
                size="sm"
                colorPalette="blue"
                onClick={() => {
                  const n = room.desks.length + 1;
                  setNewDeskName(`Desk ${n}`);
                  setAddOpen(true);
                }}
              >
                Add desk
              </Button>
            </HStack>

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
                {room.desks.map((desk) => {
                  const d = drafts[desk.id];
                  if (!d) {
                    return null;
                  }
                  return (
                    <Table.Row key={desk.id}>
                      <Table.Cell>
                        <Input
                          size="sm"
                          value={d.name}
                          onChange={(e) =>
                            setDrafts((prev) => ({
                              ...prev,
                              [desk.id]: { ...d, name: e.target.value },
                            }))
                          }
                        />
                      </Table.Cell>
                      <Table.Cell maxW="100px">
                        <Input
                          size="sm"
                          type="number"
                          min={0}
                          value={d.monitor_count}
                          onChange={(e) =>
                            setDrafts((prev) => ({
                              ...prev,
                              [desk.id]: {
                                ...d,
                                monitor_count: Number(e.target.value) || 0,
                              },
                            }))
                          }
                        />
                      </Table.Cell>
                      <Table.Cell>
                        <input
                          type="checkbox"
                          checked={d.has_keyboard}
                          onChange={(e) =>
                            setDrafts((prev) => ({
                              ...prev,
                              [desk.id]: {
                                ...d,
                                has_keyboard: e.target.checked,
                              },
                            }))
                          }
                          aria-label="Keyboard available"
                        />
                      </Table.Cell>
                      <Table.Cell>
                        <input
                          type="checkbox"
                          checked={d.has_mouse}
                          onChange={(e) =>
                            setDrafts((prev) => ({
                              ...prev,
                              [desk.id]: { ...d, has_mouse: e.target.checked },
                            }))
                          }
                          aria-label="Mouse available"
                        />
                      </Table.Cell>
                      <Table.Cell textAlign="end">
                        <HStack gap={2} justify="flex-end">
                          <Button
                            size="xs"
                            colorPalette="blue"
                            loading={patchMutation.isPending}
                            onClick={() =>
                              patchMutation.mutate({
                                deskId: desk.id,
                                body: {
                                  name: d.name,
                                  monitor_count: d.monitor_count,
                                  has_keyboard: d.has_keyboard,
                                  has_mouse: d.has_mouse,
                                  bookable: d.bookable,
                                },
                              })
                            }
                          >
                            Save
                          </Button>
                          <Button
                            size="xs"
                            colorPalette="red"
                            variant="outline"
                            onClick={() => {
                              if (window.confirm(`Delete desk ${desk.name}?`)) {
                                deleteMutation.mutate(desk.id);
                              }
                            }}
                          >
                            Delete
                          </Button>
                        </HStack>
                      </Table.Cell>
                    </Table.Row>
                  );
                })}
              </Table.Body>
            </Table.Root>
          </>
        ) : null}
      </Stack>

      <PasswordModal open={pwOpen} onOpenChange={setPwOpen} />

      <Dialog.Root open={addOpen} onOpenChange={(e) => setAddOpen(e.open)}>
        <Dialog.Backdrop />
        <Dialog.Positioner>
          <Dialog.Content maxW="md">
            <Dialog.Header>
              <Dialog.Title>Add desk</Dialog.Title>
            </Dialog.Header>
            <Dialog.Body>
              <Stack gap={2}>
                <Text fontSize="sm" fontWeight="medium">
                  Name
                </Text>
                <Input
                  value={newDeskName}
                  onChange={(e) => setNewDeskName(e.target.value)}
                />
              </Stack>
            </Dialog.Body>
            <Dialog.Footer>
              <Button variant="ghost" onClick={() => setAddOpen(false)}>
                Cancel
              </Button>
              <Button
                colorPalette="blue"
                loading={addMutation.isPending}
                disabled={!newDeskName.trim()}
                onClick={() => addMutation.mutate(newDeskName.trim())}
              >
                Add
              </Button>
            </Dialog.Footer>
          </Dialog.Content>
        </Dialog.Positioner>
      </Dialog.Root>
    </Box>
  );
}
