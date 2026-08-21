import { apiFetch } from "~/lib/fetch";
import type { JSONValue } from "~/lib/types";

export const listUsers = async (): Promise<JSONValue[]> =>
  await apiFetch<JSONValue[]>("/api/client");
