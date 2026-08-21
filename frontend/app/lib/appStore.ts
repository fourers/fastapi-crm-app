import { create } from "zustand";

export enum Status {
  success,
  error,
}

export interface AppMessage {
  id: string;
  message: string;
  status: Status;
}

interface AppState {
  messages: AppMessage[];
  addMessage: (message: Omit<AppMessage, "id">) => void;
  removeMessage: (id: string) => void;
  clearMessages: () => void;
}

export const useAppStore = create<AppState>((set) => ({
  messages: [],

  addMessage: (message) => {
    set((state) => ({
      messages: [
        ...state.messages,
        {
          ...message,
          id: crypto.randomUUID(),
        },
      ],
    }));
  },

  removeMessage: (id) => {
    set((state) => ({
      messages: state.messages.filter((message) => message.id !== id),
    }));
  },

  clearMessages: () => set({ messages: [] }),
}));
