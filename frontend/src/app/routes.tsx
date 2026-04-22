import { lazy } from 'react';

const DeskBookingPage = lazy(
  () => import('../features/deskBooking/containers/DeskBookingPage'),
);
const AdminRoomsPage = lazy(
  () => import('../features/admin/containers/AdminRoomsPage'),
);
const AdminRoomDetailPage = lazy(
  () => import('../features/admin/containers/AdminRoomDetailPage'),
);

export const routes = [
  { path: '/', element: <DeskBookingPage /> },
  { path: '/admin/rooms', element: <AdminRoomsPage /> },
  { path: '/admin/rooms/:roomId', element: <AdminRoomDetailPage /> },
];
