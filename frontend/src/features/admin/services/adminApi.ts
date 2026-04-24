import { url } from '../../deskBooking/services/deskApi';

import type { AdminDeskDto, AdminRoomDto, AdminRoomsResponse } from '../types';

async function adminFetch(
  path: string,
  getToken: () => string | null,
  init: RequestInit = {},
): Promise<Response> {
  const token = getToken();
  if (!token) {
    throw new Error('Not signed in');
  }
  const headers = new Headers(init.headers);
  headers.set('Authorization', `Bearer ${token}`);
  if (init.body !== undefined && !headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json');
  }
  return fetch(url(path), { ...init, headers });
}

async function adminJson<T>(
  path: string,
  getToken: () => string | null,
  init: RequestInit = {},
): Promise<T> {
  const res = await adminFetch(path, getToken, init);
  if (!res.ok) {
    throw new Error(await res.text());
  }
  if (res.status === 204) {
    return undefined as T;
  }
  const text = await res.text();
  if (!text) {
    return undefined as T;
  }
  return JSON.parse(text) as T;
}

export async function fetchAdminRooms(
  getToken: () => string | null,
): Promise<AdminRoomsResponse> {
  return adminJson<AdminRoomsResponse>('/admin/rooms', getToken);
}

export async function fetchAdminRoom(
  getToken: () => string | null,
  roomId: string,
): Promise<AdminRoomDto> {
  return adminJson<AdminRoomDto>(`/admin/rooms/${roomId}`, getToken);
}

export async function createAdminRoom(
  getToken: () => string | null,
  body: {
    room_number: string;
    description?: string;
    name?: string | null;
    sort_order?: number | null;
  },
): Promise<AdminRoomDto> {
  return adminJson<AdminRoomDto>('/admin/rooms', getToken, {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

export async function deleteAdminRoom(
  getToken: () => string | null,
  roomId: string,
): Promise<void> {
  await adminJson<void>(`/admin/rooms/${roomId}`, getToken, {
    method: 'DELETE',
  });
}

export async function createAdminDesk(
  getToken: () => string | null,
  roomId: string,
  body: {
    name: string;
    bookable?: boolean;
    monitor_count?: number;
    has_keyboard?: boolean;
    has_mouse?: boolean;
    sort_order?: number | null;
  },
): Promise<AdminDeskDto> {
  return adminJson<AdminDeskDto>('/admin/desks', getToken, {
    method: 'POST',
    body: JSON.stringify({ room_id: roomId, ...body }),
  });
}

export async function patchAdminDesk(
  getToken: () => string | null,
  deskId: string,
  body: Partial<{
    name: string;
    bookable: boolean;
    monitor_count: number;
    has_keyboard: boolean;
    has_mouse: boolean;
    sort_order: number;
  }>,
): Promise<AdminDeskDto> {
  return adminJson<AdminDeskDto>(`/admin/desks/${deskId}`, getToken, {
    method: 'PATCH',
    body: JSON.stringify(body),
  });
}

export async function deleteAdminDesk(
  getToken: () => string | null,
  deskId: string,
): Promise<void> {
  await adminJson<void>(`/admin/desks/${deskId}`, getToken, {
    method: 'DELETE',
  });
}
