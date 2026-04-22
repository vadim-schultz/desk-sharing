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
import { useState } from 'react';
import { Link as RouterLink } from 'react-router-dom';

import PasswordModal from '../../auth/components/PasswordModal';
import { useAuth } from '../../auth/context/AuthContext';
import {
  createAdminRoom,
  deleteAdminRoom,
  fetchAdminRooms,
} from '../services/adminApi';

export default function AdminRoomsPage() {
  const { getToken, isAuthenticated } = useAuth();
  const queryClient = useQueryClient();
  const [pwOpen, setPwOpen] = useState(false);
  const [createOpen, setCreateOpen] = useState(false);
  const [roomNumber, setRoomNumber] = useState('');
  const [description, setDescription] = useState('');

  const tokenReady = isAuthenticated && !!getToken();

  const roomsQuery = useQuery({
    queryKey: ['admin-rooms'],
    queryFn: () => fetchAdminRooms(getToken),
    enabled: tokenReady,
  });

  const createMutation = useMutation({
    mutationFn: () =>
      createAdminRoom(getToken, {
        room_number: roomNumber.trim(),
        description: description.trim(),
      }),
    onSuccess: () => {
      setCreateOpen(false);
      setRoomNumber('');
      setDescription('');
      void queryClient.invalidateQueries({ queryKey: ['admin-rooms'] });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (roomId: string) => deleteAdminRoom(getToken, roomId),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ['admin-rooms'] });
    },
  });

  if (!tokenReady) {
    return (
      <Box maxW="720px" mx="auto" py={8} px={4}>
        <Stack gap={4}>
          <Heading size="lg">Admin: rooms</Heading>
          <Text color="fg.muted">
            Sign in with the admin password to edit rooms and desks.
          </Text>
          <Button colorPalette="blue" w="fit-content" onClick={() => setPwOpen(true)}>
            Sign in to admin
          </Button>
        </Stack>
        <PasswordModal open={pwOpen} onOpenChange={setPwOpen} />
      </Box>
    );
  }

  return (
    <Box maxW="960px" mx="auto" py={8} px={4}>
      <Stack gap={6}>
        <HStack justify="space-between" flexWrap="wrap" gap={3}>
          <Heading size="lg">Admin: rooms & desks</Heading>
          <Button colorPalette="blue" onClick={() => setCreateOpen(true)}>
            Add room
          </Button>
        </HStack>

        {roomsQuery.isPending ? (
          <HStack>
            <Spinner size="sm" />
            <Text>Loading…</Text>
          </HStack>
        ) : null}
        {roomsQuery.isError ? (
          <Text color="red.fg" whiteSpace="pre-wrap">
            {roomsQuery.error instanceof Error
              ? roomsQuery.error.message
              : String(roomsQuery.error)}
          </Text>
        ) : null}

        {roomsQuery.data ? (
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
              {roomsQuery.data.rooms.map((room) => (
                <Table.Row key={room.id}>
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
                      <Button
                        size="xs"
                        colorPalette="red"
                        variant="outline"
                        onClick={() => {
                          if (
                            window.confirm(
                              `Delete room ${room.room_number} and all its desks?`,
                            )
                          ) {
                            deleteMutation.mutate(room.id);
                          }
                        }}
                      >
                        Delete
                      </Button>
                    </HStack>
                  </Table.Cell>
                </Table.Row>
              ))}
            </Table.Body>
          </Table.Root>
        ) : null}

        {roomsQuery.data && roomsQuery.data.rooms.length === 0 ? (
          <Text color="fg.muted">No rooms yet. Add one to get started.</Text>
        ) : null}
      </Stack>

      <Dialog.Root open={createOpen} onOpenChange={(e) => setCreateOpen(e.open)}>
        <Dialog.Backdrop />
        <Dialog.Positioner>
          <Dialog.Content maxW="md">
            <Dialog.Header>
              <Dialog.Title>Add room</Dialog.Title>
            </Dialog.Header>
            <Dialog.Body>
              <Stack gap={3}>
                <Stack gap={1}>
                  <Text fontSize="sm" fontWeight="medium">
                    Room number
                  </Text>
                  <Input
                    value={roomNumber}
                    onChange={(e) => setRoomNumber(e.target.value)}
                    placeholder="e.g. 3.12"
                  />
                </Stack>
                <Stack gap={1}>
                  <Text fontSize="sm" fontWeight="medium">
                    Description
                  </Text>
                  <Input
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    placeholder="Short description"
                  />
                </Stack>
              </Stack>
            </Dialog.Body>
            <Dialog.Footer>
              <Button variant="ghost" onClick={() => setCreateOpen(false)}>
                Cancel
              </Button>
              <Button
                colorPalette="blue"
                loading={createMutation.isPending}
                disabled={!roomNumber.trim()}
                onClick={() => createMutation.mutate()}
              >
                Create
              </Button>
            </Dialog.Footer>
          </Dialog.Content>
        </Dialog.Positioner>
      </Dialog.Root>
    </Box>
  );
}
