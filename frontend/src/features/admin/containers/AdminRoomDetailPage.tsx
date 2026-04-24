import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

import { useAuth } from '../../auth/context/AuthContext';
import AdminSignInGate from '../components/AdminSignInGate';
import AdminRoomDetailView from '../components/room-detail/AdminRoomDetailView';
import type { DeskDraft } from '../components/room-detail/types';
import {
  createAdminDesk,
  deleteAdminDesk,
  fetchAdminRoom,
  patchAdminDesk,
} from '../services/adminApi';

export default function AdminRoomDetailPage() {
  const { roomId } = useParams<{ roomId: string }>();
  const { getToken, isAuthenticated } = useAuth();
  const queryClient = useQueryClient();
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
    mutationFn: ({
      deskId,
      body,
    }: {
      deskId: string;
      body: Partial<DeskDraft>;
    }) => patchAdminDesk(getToken, deskId, body),
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
      <AdminSignInGate
        title="Admin: room"
        description="Sign in to edit desks."
      />
    );
  }

  const room = roomQuery.data;

  return (
    <AdminRoomDetailView
      isPending={roomQuery.isPending}
      isError={roomQuery.isError}
      error={roomQuery.error}
      room={room}
      drafts={drafts}
      onDraftChange={(deskId, patch) =>
        setDrafts((prev) => ({
          ...prev,
          [deskId]: { ...prev[deskId]!, ...patch },
        }))
      }
      onSaveDesk={(deskId, body) => patchMutation.mutate({ deskId, body })}
      savePending={patchMutation.isPending}
      onDeleteDesk={(deskId) => deleteMutation.mutate(deskId)}
      onRequestAddDesk={() => {
        if (!room) {
          return;
        }
        const n = room.desks.length + 1;
        setNewDeskName(`Desk ${n}`);
        setAddOpen(true);
      }}
      addOpen={addOpen}
      onAddOpenChange={setAddOpen}
      newDeskName={newDeskName}
      onNewDeskNameChange={setNewDeskName}
      onConfirmAddDesk={() => addMutation.mutate(newDeskName.trim())}
      addPending={addMutation.isPending}
    />
  );
}
