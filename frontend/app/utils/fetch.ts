import { useErrorStore } from "~/stores/errorStore";

export async function apiFetch<T>(input: RequestInfo | URL, init?: RequestInit): Promise<T | null> {
  try {
    const response = await fetch(input, init);

    if (response.ok) {
      return response.json();
    } else {
      const text = await response.text();

      useErrorStore.getState().addError({
        status: response.status,
        message: text || response.statusText,
      });
    }
  } catch (error) {
    useErrorStore.getState().addError({
      message: error instanceof Error ? error.message : "Unknown error",
    });
  }
  return null;
}
