import { Text } from '@chakra-ui/react';

interface DeskBookingSameDayNoteProps {
  show: boolean;
  timezone: string;
}

export default function DeskBookingSameDayNote({
  show,
  timezone,
}: DeskBookingSameDayNoteProps) {
  if (!show) {
    return null;
  }
  return (
    <Text color="fg.muted" fontSize="sm">
      Same-day bookings are not available after 10:00 ({timezone}).
    </Text>
  );
}
