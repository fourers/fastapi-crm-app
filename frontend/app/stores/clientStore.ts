import { create } from "zustand";

import { apiFetch } from "~/utils/fetch";

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
  loadClients: () => Promise<void>;
}

export const useClientStore = create<ClientStore>((set) => ({
  clients: [],
  loading: true,

  loadClients: async () => {
    set({ loading: true });

    const response = await apiFetch<Client[]>("/api/clients");
    if (response !== null) {
      set({
        clients: response,
        loading: false,
      });
    } else {
      set({
        loading: false,
      });
    }
  },
}));
