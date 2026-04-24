import { Button, Heading, HStack } from '@chakra-ui/react';

interface RoomsListToolbarProps {
  onRequestCreateRoom: () => void;
}

export default function RoomsListToolbar({ onRequestCreateRoom }: RoomsListToolbarProps) {
  return (
    <HStack justify="space-between" flexWrap="wrap" gap={3}>
      <Heading size="lg">Admin: rooms & desks</Heading>
      <Button colorPalette="blue" onClick={onRequestCreateRoom}>
        Add room
      </Button>
    </HStack>
  );
}
