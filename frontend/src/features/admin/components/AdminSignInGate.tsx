import { Box, Button, Heading, Stack, Text } from '@chakra-ui/react';
import { useState } from 'react';

import PasswordModal from '../../auth/components/PasswordModal';

interface AdminSignInGateProps {
  title: string;
  description: string;
}

/** Shown when the user must authenticate before using an admin screen. */
export default function AdminSignInGate({
  title,
  description,
}: AdminSignInGateProps) {
  const [pwOpen, setPwOpen] = useState(false);

  return (
    <Box maxW="720px" mx="auto" py={8} px={4}>
      <Stack gap={4}>
        <Heading size="lg">{title}</Heading>
        <Text color="fg.muted">{description}</Text>
        <Button
          colorPalette="blue"
          w="fit-content"
          onClick={() => setPwOpen(true)}
        >
          Sign in to admin
        </Button>
      </Stack>
      <PasswordModal open={pwOpen} onOpenChange={setPwOpen} />
    </Box>
  );
}
