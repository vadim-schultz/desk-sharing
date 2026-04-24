import { HStack, Spinner, Text } from '@chakra-ui/react';

interface RoomDetailQueryStatusProps {
  isPending: boolean;
  isError: boolean;
  error: unknown;
}

export default function RoomDetailQueryStatus({
  isPending,
  isError,
  error,
}: RoomDetailQueryStatusProps) {
  return (
    <>
      {isPending ? (
        <HStack>
          <Spinner size="sm" />
          <Text>Loading…</Text>
        </HStack>
      ) : null}
      {isError ? (
        <Text color="red.fg" whiteSpace="pre-wrap">
          {error instanceof Error ? error.message : String(error)}
        </Text>
      ) : null}
    </>
  );
}
