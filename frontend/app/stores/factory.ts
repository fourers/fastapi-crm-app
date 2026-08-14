import { create } from "zustand";

import { apiFetch } from "~/utils/fetch";

interface Store<T> {
  data: T;
  loading: boolean;
  loadData: () => Promise<void>;
}

export const createStore = <T>(endpoint: string, initialData: T) =>
  create<Store<T>>((set) => ({
    data: initialData,
    loading: true,

    loadData: async () => {
      set({ loading: true });

      const response = await apiFetch<T>(endpoint);
      if (response !== null) {
        set({
          data: response,
          loading: false,
        });
      } else {
        set({
          loading: false,
        });
      }
    },
  }));
