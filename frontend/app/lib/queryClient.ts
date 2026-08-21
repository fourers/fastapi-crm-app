import { MutationCache, QueryCache, QueryClient } from "@tanstack/react-query";

import { Status, useAppStore } from "~/lib/appStore";

const commonErrorHandler = (error: Error) =>
  useAppStore.getState().addMessage({
    status: Status.error,
    message: error.message,
  });

export const queryClient = new QueryClient({
  queryCache: new QueryCache({
    onError: commonErrorHandler,
  }),
  mutationCache: new MutationCache({
    onError: commonErrorHandler,
  }),
  defaultOptions: {
    queries: {
      retry: false,
      staleTime: Infinity,
      refetchOnMount: "always",
    },
  },
});
