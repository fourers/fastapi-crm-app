import { formatResponse } from "~/lib/formatters";
import { ApiError } from "~/lib/types";

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
