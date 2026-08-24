import { apiFetch } from "~/lib/fetch";
import type { JSONValue } from "~/lib/types";

export const listGroups = async (): Promise<JSONValue[]> =>
  await apiFetch<JSONValue[]>("/api/group");
