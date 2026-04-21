import { lazy } from 'react';

const DeskBookingPage = lazy(
  () => import('../features/deskBooking/containers/DeskBookingPage'),
);

export const routes = [{ path: '/', element: <DeskBookingPage /> }];
