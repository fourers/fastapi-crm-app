import type { JSONValue } from "~/utils/types";

export async function apiFetch<T>(
  input: RequestInfo | URL,
  init?: RequestInit,
): Promise<T> {
  const response = await fetch(input, init);

  if (!response.ok) {
    throw new Error(await formatResponse(response));
  }

  return response.json();
}

async function formatResponse(response: Response): Promise<string> {
  const prefix = response.status ? `${response.status}: ` : "";

  const payload = await response.json().catch(() => null);
  if (payload?.detail) {
    if (Array.isArray(payload.detail)) {
      return `${prefix}${payload.detail
        .map((item: JSONValue) => item.summary ?? JSON.stringify(item))
        .join("; ")}`;
    }

    if (typeof payload.detail === "string") {
      return `${prefix}${payload.detail}`;
    }
  }

  const text = await response.text();
  return `${prefix}${text ?? response.statusText}`;
}
