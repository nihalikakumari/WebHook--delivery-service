import { RouterProvider, createRouter } from '@tanstack/react-router';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { rootRoute } from './routes/root';
import { subscriptionsRoute } from './routes/subscriptions';
import { logsRoute } from './routes/logs';

const queryClient = new QueryClient();

const routeTree = rootRoute.addChildren([
  subscriptionsRoute,
  logsRoute,
]);

const router = createRouter({ routeTree });

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  );
}

export default App;