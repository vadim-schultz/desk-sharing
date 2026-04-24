import { HStack, Spinner, Text } from '@chakra-ui/react';

interface DeskBookingQueryStatusProps {
  loading: boolean;
  isError: boolean;
  error: unknown;
}

export default function DeskBookingQueryStatus({
  loading,
  isError,
  error,
}: DeskBookingQueryStatusProps) {
  return (
    <>
      {loading ? (
        <HStack>
          <Spinner size="sm" />
          <Text>Loading…</Text>
        </HStack>
      ) : null}
      {isError && error ? (
        <Text color="red.fg" whiteSpace="pre-wrap">
          {error instanceof Error ? error.message : String(error)}
        </Text>
      ) : null}
    </>
  );
}
