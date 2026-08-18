import { QueryCache, QueryClient } from "@tanstack/react-query";

import { Status, useAppStore } from "~/stores/appStore";

export const queryClient = new QueryClient({
  queryCache: new QueryCache({
    onError: (error) => {
      useAppStore.getState().addMessage({
        status: Status.error,
        message: error.message,
      });
    },
  }),
  defaultOptions: {
    queries: {
      staleTime: Infinity,
    },
  },
});
