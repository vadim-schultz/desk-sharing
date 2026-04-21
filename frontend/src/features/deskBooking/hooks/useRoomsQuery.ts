import { useQuery } from '@tanstack/react-query';

import { fetchRooms } from '../services/deskApi';

export function useRoomsQuery(viewDate: string) {
  return useQuery({
    queryKey: ['rooms', viewDate || null],
    queryFn: () => fetchRooms(viewDate || undefined),
  });
}
