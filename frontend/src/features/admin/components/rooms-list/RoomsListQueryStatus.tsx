import { HStack, Spinner, Text } from '@chakra-ui/react';

interface RoomsListQueryStatusProps {
  isPending: boolean;
  isError: boolean;
  error: unknown;
}

export default function RoomsListQueryStatus({
  isPending,
  isError,
  error,
}: RoomsListQueryStatusProps) {
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
