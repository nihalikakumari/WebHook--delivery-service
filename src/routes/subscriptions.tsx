import { createRoute } from '@tanstack/react-router';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useForm } from 'react-hook-form';
import { Plus, Trash2 } from 'lucide-react';
import { rootRoute } from './root';
import { api } from '../lib/api';

interface Subscription {
  id: number;
  name: string;
  target_url: string;
  secret_key?: string;
  event_types?: string[];
  is_active: boolean;
}

interface SubscriptionForm {
  name: string;
  target_url: string;
  secret_key?: string;
  event_types?: string;
}

export const subscriptionsRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/',
  component: SubscriptionsPage,
});

function SubscriptionsPage() {
  const queryClient = useQueryClient();
  const { register, handleSubmit, reset } = useForm<SubscriptionForm>();

  const { data: subscriptions, isLoading } = useQuery({
    queryKey: ['subscriptions'],
    queryFn: () => api.get('/subscriptions').then(res => res.data),
  });

  const createMutation = useMutation({
    mutationFn: (data: SubscriptionForm) => 
      api.post('/subscriptions', {
        ...data,
        event_types: data.event_types?.split(',').map(t => t.trim()),
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['subscriptions'] });
      reset();
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (id: number) => api.delete(`/subscriptions/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['subscriptions'] });
    },
  });

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="bg-white shadow sm:rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg font-medium leading-6 text-gray-900">
            Create New Subscription
          </h3>
          <form 
            onSubmit={handleSubmit((data) => createMutation.mutate(data))}
            className="mt-5 space-y-4"
          >
            <div>
              <label className="block text-sm font-medium text-gray-700">
                Name
              </label>
              <input
                type="text"
                {...register('name')}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">
                Target URL
              </label>
              <input
                type="url"
                {...register('target_url')}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">
                Secret Key (Optional)
              </label>
              <input
                type="text"
                {...register('secret_key')}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">
                Event Types (Optional, comma-separated)
              </label>
              <input
                type="text"
                {...register('event_types')}
                placeholder="order.created, user.updated"
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
              />
            </div>
            <button
              type="submit"
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              <Plus className="h-4 w-4 mr-2" />
              Create Subscription
            </button>
          </form>
        </div>
      </div>

      <div className="bg-white shadow sm:rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg font-medium leading-6 text-gray-900">
            Active Subscriptions
          </h3>
          <div className="mt-5 space-y-4">
            {subscriptions?.map((sub: Subscription) => (
              <div
                key={sub.id}
                className="border rounded-lg p-4 flex justify-between items-center"
              >
                <div>
                  <h4 className="font-medium">{sub.name}</h4>
                  <p className="text-sm text-gray-500">{sub.target_url}</p>
                  {sub.event_types && (
                    <div className="mt-2 flex gap-2">
                      {sub.event_types.map((type) => (
                        <span
                          key={type}
                          className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                        >
                          {type}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
                <button
                  onClick={() => deleteMutation.mutate(sub.id)}
                  className="text-red-600 hover:text-red-800"
                >
                  <Trash2 className="h-5 w-5" />
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}