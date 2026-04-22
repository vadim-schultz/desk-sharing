export interface AdminDeskDto {
  id: string;
  name: string;
  bookable: boolean;
  monitor_count: number;
  has_keyboard: boolean;
  has_mouse: boolean;
  sort_order: number;
}

export interface AdminRoomDto {
  id: string;
  room_number: string;
  description: string;
  name: string;
  sort_order: number;
  desks: AdminDeskDto[];
}

export interface AdminRoomsResponse {
  rooms: AdminRoomDto[];
}
