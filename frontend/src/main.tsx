import { Suspense, lazy } from 'react';
import { createRoot } from 'react-dom/client';

import './style.css';

const AppBootstrap = lazy(() => import('./app/AppBootstrap'));

export const MinimalAppShell = () => (
  <div
    style={{
      minHeight: '100vh',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      gap: '12px',
      background:
        'radial-gradient(circle at 20% 20%, #f3f6fb 0, transparent 25%), #ffffff',
      color: '#1a202c',
      fontFamily:
        'Inter, system-ui, -apple-system, BlinkMacSystemFont, sans-serif',
      textAlign: 'center',
      padding: '24px',
    }}
  >
    <style>
      {`
        @keyframes app-shell-spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}
    </style>
    <div style={{ fontSize: '22px', fontWeight: 700 }}>Desk sharing</div>
    <div
      role="status"
      aria-label="Loading interface"
      style={{
        width: '36px',
        height: '36px',
        borderRadius: '50%',
        border: '3px solid #cbd5e1',
        borderTopColor: '#2563eb',
        animation: 'app-shell-spin 0.9s linear infinite',
      }}
    />
    <div style={{ color: '#4a5568', fontSize: '15px' }}>
      Loading interface...
    </div>
  </div>
);

createRoot(document.getElementById('root')!).render(
  <Suspense fallback={<MinimalAppShell />}>
    <AppBootstrap />
  </Suspense>,
);
