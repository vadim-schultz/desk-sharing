import { Button, Dialog, Input, Stack, Text } from '@chakra-ui/react';

interface AddRoomDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  roomNumber: string;
  onRoomNumberChange: (value: string) => void;
  description: string;
  onDescriptionChange: (value: string) => void;
  onConfirmCreate: () => void;
  createPending: boolean;
}

export default function AddRoomDialog({
  open,
  onOpenChange,
  roomNumber,
  onRoomNumberChange,
  description,
  onDescriptionChange,
  onConfirmCreate,
  createPending,
}: AddRoomDialogProps) {
  return (
    <Dialog.Root open={open} onOpenChange={(e) => onOpenChange(e.open)}>
      <Dialog.Backdrop />
      <Dialog.Positioner>
        <Dialog.Content maxW="md">
          <Dialog.Header>
            <Dialog.Title>Add room</Dialog.Title>
          </Dialog.Header>
          <Dialog.Body>
            <Stack gap={3}>
              <Stack gap={1}>
                <Text fontSize="sm" fontWeight="medium">
                  Room number
                </Text>
                <Input
                  value={roomNumber}
                  onChange={(e) => onRoomNumberChange(e.target.value)}
                  placeholder="e.g. 3.12"
                />
              </Stack>
              <Stack gap={1}>
                <Text fontSize="sm" fontWeight="medium">
                  Description
                </Text>
                <Input
                  value={description}
                  onChange={(e) => onDescriptionChange(e.target.value)}
                  placeholder="Short description"
                />
              </Stack>
            </Stack>
          </Dialog.Body>
          <Dialog.Footer>
            <Button variant="ghost" onClick={() => onOpenChange(false)}>
              Cancel
            </Button>
            <Button
              colorPalette="blue"
              loading={createPending}
              disabled={!roomNumber.trim()}
              onClick={onConfirmCreate}
            >
              Create
            </Button>
          </Dialog.Footer>
        </Dialog.Content>
      </Dialog.Positioner>
    </Dialog.Root>
  );
}
