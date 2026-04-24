import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useState } from 'react';

import { useAuth } from '../../auth/context/AuthContext';
import AdminSignInGate from '../components/AdminSignInGate';
import AdminRoomsListView from '../components/rooms-list/AdminRoomsListView';
import {
  createAdminRoom,
  deleteAdminRoom,
  fetchAdminRooms,
} from '../services/adminApi';

export default function AdminRoomsPage() {
  const { getToken, isAuthenticated } = useAuth();
  const queryClient = useQueryClient();
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
      <AdminSignInGate
        title="Admin: rooms"
        description="Sign in with the admin password to edit rooms and desks."
      />
    );
  }

  return (
    <AdminRoomsListView
      isPending={roomsQuery.isPending}
      isError={roomsQuery.isError}
      error={roomsQuery.error}
      rooms={roomsQuery.data?.rooms}
      onRequestCreateRoom={() => setCreateOpen(true)}
      onDeleteRoom={(roomId) => deleteMutation.mutate(roomId)}
      createOpen={createOpen}
      onCreateOpenChange={setCreateOpen}
      roomNumber={roomNumber}
      onRoomNumberChange={setRoomNumber}
      description={description}
      onDescriptionChange={setDescription}
      onConfirmCreateRoom={() => createMutation.mutate()}
      createPending={createMutation.isPending}
    />
  );
}
