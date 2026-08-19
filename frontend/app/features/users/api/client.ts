import { apiFetch } from "~/utils/fetch";
import type { JSONValue } from "~/utils/types";

export const listUsers = async (): Promise<JSONValue[]> =>
  await apiFetch<JSONValue[]>("/api/client");
