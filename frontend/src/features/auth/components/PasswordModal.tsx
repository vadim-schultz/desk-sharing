import { Button, Dialog, Input, Stack, Text } from '@chakra-ui/react';
import { useRef, useState } from 'react';

import { useAuth } from '../context/AuthContext';

interface PasswordModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSuccess?: (token: string) => void;
}

const PasswordModal = ({
  open,
  onOpenChange,
  onSuccess,
}: PasswordModalProps) => {
  const { authenticate } = useAuth();
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleSubmit = async () => {
    if (!password.trim()) {
      return;
    }
    setLoading(true);
    setError('');
    try {
      const token = await authenticate(password);
      setPassword('');
      onSuccess?.(token);
      onOpenChange(false);
    } catch (err: unknown) {
      const message =
        err instanceof Error ? err.message : 'Authentication failed';
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setPassword('');
    setError('');
  };

  return (
    <Dialog.Root
      open={open}
      onOpenChange={(e) => {
        if (!e.open) {
          reset();
        }
        onOpenChange(e.open);
      }}
      initialFocusEl={() => inputRef.current}
    >
      <Dialog.Backdrop />
      <Dialog.Positioner>
        <Dialog.Content maxW="420px" w="90vw">
          <Dialog.Header>
            <Dialog.Title>Admin sign-in</Dialog.Title>
          </Dialog.Header>
          <Dialog.Body>
            <Stack gap={3}>
              <Text fontSize="sm" color="fg.muted">
                Enter the admin password to manage rooms and desks.
              </Text>
              <Input
                ref={inputRef}
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    void handleSubmit();
                  }
                }}
              />
              {error ? (
                <Text fontSize="sm" color="red.fg">
                  {error}
                </Text>
              ) : null}
            </Stack>
          </Dialog.Body>
          <Dialog.Footer>
            <Button
              variant="ghost"
              mr="auto"
              onClick={() => onOpenChange(false)}
            >
              Cancel
            </Button>
            <Button
              colorPalette="blue"
              loading={loading}
              disabled={!password.trim() || loading}
              onClick={() => void handleSubmit()}
            >
              Sign in
            </Button>
          </Dialog.Footer>
        </Dialog.Content>
      </Dialog.Positioner>
    </Dialog.Root>
  );
};

export default PasswordModal;
