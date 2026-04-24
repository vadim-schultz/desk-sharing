import { Button } from '@chakra-ui/react';
import { Link as RouterLink } from 'react-router-dom';

export default function RoomDetailBackNav() {
  return (
    <RouterLink to="/admin/rooms">
      <Button variant="ghost" alignSelf="flex-start">
        ← Back to rooms
      </Button>
    </RouterLink>
  );
}
