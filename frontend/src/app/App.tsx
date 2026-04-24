import { Suspense } from 'react';
import { Route, Routes } from 'react-router-dom';

import AppLayout from '../components/layout/AppLayout';
import LoadingSkeleton from '../components/feedback/LoadingSkeleton';
import { routes } from './routes';

function App() {
  return (
    <AppLayout>
      <Suspense
        fallback={<LoadingSkeleton isFullPage label="Loading application" />}
      >
        <Routes>
          {routes.map((route) => (
            <Route key={route.path} path={route.path} element={route.element} />
          ))}
        </Routes>
      </Suspense>
    </AppLayout>
  );
}

export default App;
