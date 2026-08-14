import { create } from "zustand";

import { apiFetch } from "~/utils/fetch";
import { type JSONValue } from "~/utils/types";

interface UserStore {
  users: JSONValue[];
  loading: boolean;
  loadUsers: () => Promise<void>;
}

export const useUserStore = create<UserStore>((set) => ({
  users: [],
  loading: true,

  loadUsers: async () => {
    set({ loading: true });

    const response = await apiFetch<JSONValue[]>("/api/user");
    if (response !== null) {
      set({
        users: response,
        loading: false,
      });
    } else {
      set({
        loading: false,
      });
    }
  },
}));
