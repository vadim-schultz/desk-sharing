import { Box, Container, Heading, HStack, VStack } from '@chakra-ui/react';
import type { ReactNode } from 'react';
import { Link as RouterLink } from 'react-router-dom';

import ColorModeToggle from './ColorModeToggle';

interface AppLayoutProps {
  children: ReactNode;
}

const AppLayout = ({ children }: AppLayoutProps) => {
  return (
    <VStack align="stretch" minH="100vh" gap={0} bg="bg">
      <Box
        as="header"
        bg="bg.subtle"
        borderBottomWidth="1px"
        borderColor="border"
        position="sticky"
        top={0}
        zIndex="sticky"
      >
        <Container maxW="container.xl" py={4}>
          <HStack justify="space-between">
            <RouterLink
              to="/"
              style={{ textDecoration: 'none', color: 'inherit' }}
            >
              <Heading size="md">Desk sharing</Heading>
            </RouterLink>
            <ColorModeToggle />
          </HStack>
        </Container>
      </Box>

      <Box as="main" flex="1" bg="bg">
        <Container maxW="container.xl" py={8}>
          {children}
        </Container>
      </Box>
    </VStack>
  );
};

export default AppLayout;
