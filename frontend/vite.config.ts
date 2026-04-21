import react from '@vitejs/plugin-react';
import { defineConfig } from 'vite';

const api = process.env.VITE_DEV_API_PROXY ?? 'http://127.0.0.1:8000';

export default defineConfig({
  plugins: [react()],
  optimizeDeps: {
    include: [
      'react',
      'react-dom',
      'react-router-dom',
      '@chakra-ui/react',
      '@emotion/react',
      '@emotion/styled',
    ],
  },
  server: {
    proxy: {
      '/api': {
        target: api,
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
});
