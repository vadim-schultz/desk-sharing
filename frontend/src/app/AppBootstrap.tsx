import { ChakraProvider, defaultSystem } from '@chakra-ui/react';
import { QueryClientProvider } from '@tanstack/react-query';
import { StrictMode } from 'react';
import { BrowserRouter } from 'react-router-dom';

import { ColorModeProvider } from '../components/ui/color-mode';
import { queryClient } from './queryClient';
import App from './App';

/**
 * Bundles Chakra + routing providers so they can be lazy loaded together.
 */
const AppBootstrap = () => (
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <ChakraProvider value={defaultSystem}>
        <ColorModeProvider>
          <BrowserRouter>
            <App />
          </BrowserRouter>
        </ColorModeProvider>
      </ChakraProvider>
    </QueryClientProvider>
  </StrictMode>
);

export default AppBootstrap;
