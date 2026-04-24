import {
  Box,
  Button,
  Container,
  Heading,
  HStack,
  Menu,
  Portal,
  VStack,
} from '@chakra-ui/react';
import type { ReactNode } from 'react';
import { useState } from 'react';
import { FaUser } from 'react-icons/fa';
import { Link as RouterLink, useNavigate } from 'react-router-dom';

import PasswordModal from '../../features/auth/components/PasswordModal';
import { useAuth } from '../../features/auth/context/AuthContext';
import ColorModeToggle from './ColorModeToggle';

interface AppLayoutProps {
  children: ReactNode;
}

const AppLayout = ({ children }: AppLayoutProps) => {
  const navigate = useNavigate();
  const { isAuthenticated, clearToken } = useAuth();
  const [pwOpen, setPwOpen] = useState(false);

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
            <HStack gap={1}>
              <Menu.Root positioning={{ placement: 'bottom-end' }}>
                <Menu.Trigger asChild>
                  <Button
                    aria-label="Account menu"
                    variant="ghost"
                    size="sm"
                    colorPalette="gray"
                  >
                    <FaUser />
                  </Button>
                </Menu.Trigger>
                <Portal>
                  <Menu.Positioner>
                    <Menu.Content minW="220px">
                      <Menu.Item
                        value="admin"
                        onClick={() => navigate('/admin/rooms')}
                      >
                        Admin: rooms & desks
                      </Menu.Item>
                      {isAuthenticated ? (
                        <Menu.Item value="signout" onClick={() => clearToken()}>
                          Sign out of admin
                        </Menu.Item>
                      ) : (
                        <Menu.Item
                          value="signin"
                          onClick={() => setPwOpen(true)}
                        >
                          Sign in to admin…
                        </Menu.Item>
                      )}
                    </Menu.Content>
                  </Menu.Positioner>
                </Portal>
              </Menu.Root>
              <ColorModeToggle />
            </HStack>
          </HStack>
        </Container>
      </Box>

      <Box as="main" flex="1" bg="bg">
        <Container maxW="container.xl" py={8}>
          {children}
        </Container>
      </Box>

      <PasswordModal open={pwOpen} onOpenChange={setPwOpen} />
    </VStack>
  );
};

export default AppLayout;
