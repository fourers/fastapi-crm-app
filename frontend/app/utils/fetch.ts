import { Status, useAppStore } from "~/stores/appStore";

export async function apiFetch<T>(
  input: RequestInfo | URL,
  init?: RequestInit,
): Promise<T | null> {
  try {
    const response = await fetch(input, init);

    if (response.ok) {
      return response.json();
    } else {
      useAppStore.getState().addMessage({
        message: await formatResponse(response),
        status: Status.error,
      });
    }
  } catch (error) {
    useAppStore.getState().addMessage({
      message: error instanceof Error ? error.message : "Unknown error",
      status: Status.error,
    });
  }
  return null;
}

async function formatResponse(response: Response): Promise<string> {
  const prefix = response.status ? `${response.status}: ` : "";
  const text = await response.text();
  return `${prefix}${text || response.statusText}`;
}
