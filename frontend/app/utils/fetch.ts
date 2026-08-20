import { ApiError, type JSONValue } from "~/utils/types";

export const apiFetch = async <T>(
  input: RequestInfo | URL,
  init?: RequestInit,
): Promise<T> => {
  const response = await fetch(input, init);

  if (!response.ok) {
    throw new ApiError(response.status, await formatResponse(response));
  }

  return response.json();
};

const formatResponse = async (response: Response): Promise<string> => {
  const prefix = `${response.status} Error`;

  const payload = await response.json().catch(() => null);
  if (payload?.detail) {
    if (Array.isArray(payload.detail)) {
      return `${prefix}\n${payload.detail
        .map((item: JSONValue) => item.summary ?? JSON.stringify(item))
        .join("\n")}`;
    }

    if (typeof payload.detail === "string") {
      return `${prefix}\n${payload.detail}`;
    }
  }

  const text = await response.text();
  return `${prefix}\n${text ?? response.statusText}`;
};
