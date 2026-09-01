import type { SearchResult } from "~/features/search/api/types";
import { apiFetch } from "~/lib/fetch";
import { formatName } from "~/lib/formatters";
import type { JSONValue } from "~/lib/types";

export const listUsers = async (): Promise<JSONValue[]> =>
  await apiFetch<JSONValue[]>("/api/user");

export const searchUsers = async (q: string): Promise<SearchResult[]> => {
  const response = await apiFetch<JSONValue[]>(
    `/api/user/search?q=${encodeURIComponent(q)}`,
  );
  return response.map((value) => ({
    id: value.id as string,
    name: formatName(value),
  }));
};
