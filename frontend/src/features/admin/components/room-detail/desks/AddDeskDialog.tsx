import { Button, Dialog, Input, Stack, Text } from '@chakra-ui/react';

interface AddDeskDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  newDeskName: string;
  onNewDeskNameChange: (name: string) => void;
  onConfirmAdd: () => void;
  addPending: boolean;
}

export default function AddDeskDialog({
  open,
  onOpenChange,
  newDeskName,
  onNewDeskNameChange,
  onConfirmAdd,
  addPending,
}: AddDeskDialogProps) {
  return (
    <Dialog.Root open={open} onOpenChange={(e) => onOpenChange(e.open)}>
      <Dialog.Backdrop />
      <Dialog.Positioner>
        <Dialog.Content maxW="md">
          <Dialog.Header>
            <Dialog.Title>Add desk</Dialog.Title>
          </Dialog.Header>
          <Dialog.Body>
            <Stack gap={2}>
              <Text fontSize="sm" fontWeight="medium">
                Name
              </Text>
              <Input
                value={newDeskName}
                onChange={(e) => onNewDeskNameChange(e.target.value)}
              />
            </Stack>
          </Dialog.Body>
          <Dialog.Footer>
            <Button variant="ghost" onClick={() => onOpenChange(false)}>
              Cancel
            </Button>
            <Button
              colorPalette="blue"
              loading={addPending}
              disabled={!newDeskName.trim()}
              onClick={onConfirmAdd}
            >
              Add
            </Button>
          </Dialog.Footer>
        </Dialog.Content>
      </Dialog.Positioner>
    </Dialog.Root>
  );
}
