import { create } from "zustand";

export interface Client {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  owner_id: string;
}

interface ClientStore {
  clients: Client[];
  loading: boolean;
  error: string | null;
  loadClient: () => Promise<void>;
}

export const useClientStore = create<ClientStore>((set) => ({
  clients: [],
  loading: false,
  error: null,

  loadClient: async () => {
    set({ loading: true, error: null });

    try {
      const response = await fetch("/api/client");

      if (!response.ok) {
        throw new Error(`Request failed: ${response.status}`);
      }

      const clients = await response.json();

      set({
        clients,
        loading: false,
      });
    } catch (error) {
      set({
        loading: false,
        error: error instanceof Error ? error.message : "Unknown error",
      });
    }
  },
}));
