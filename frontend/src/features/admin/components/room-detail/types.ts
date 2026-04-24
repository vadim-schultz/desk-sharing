import type { AdminDeskDto } from '../../types';

export type DeskDraft = Pick<
  AdminDeskDto,
  'name' | 'monitor_count' | 'has_keyboard' | 'has_mouse' | 'bookable'
>;
