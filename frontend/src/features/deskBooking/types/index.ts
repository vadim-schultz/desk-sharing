export type DeskDayStatus = 'unavailable' | 'bookable' | 'pending' | 'booked';

export interface DeskDto {
  id: string;
  name: string;
  bookable: boolean;
  monitor_count: number;
  has_keyboard: boolean;
  has_mouse: boolean;
  status: DeskDayStatus;
  booking_id: string | null;
}

export interface RoomDto {
  id: string;
  room_number: string;
  description: string;
  name: string;
  desks: DeskDto[];
}

export interface RoomsResponse {
  date: string;
  timezone: string;
  rooms: RoomDto[];
}
