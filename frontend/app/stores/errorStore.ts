import { create } from "zustand";

interface AppError {
  id: string;
  message: string;
  status?: number;
}

interface ErrorState {
  errors: AppError[];
  addError: (error: Omit<AppError, "id">) => void;
  removeError: (id: string) => void;
  clearErrors: () => void;
}

export const useErrorStore = create<ErrorState>((set) => ({
  errors: [],

  addError: (error) =>
    set((state) => ({
      errors: [
        ...state.errors,
        {
          ...error,
          id: crypto.randomUUID(),
        },
      ],
    })),

  removeError: (id) =>
    set((state) => ({
      errors: state.errors.filter((error) => error.id !== id),
    })),

  clearErrors: () => set({ errors: [] }),
}));
