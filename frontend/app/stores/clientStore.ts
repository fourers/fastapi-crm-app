import { createStore } from "~/stores/factory";

export interface Client {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  owner_id: string;
}

export const useClientStore = createStore<Client[]>("/api/client", []);
