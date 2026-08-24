import { apiFetch, apiFetchNullable } from "~/lib/fetch";
import type { JSONValue } from "~/lib/types";

export const listGroups = async (): Promise<JSONValue[]> =>
  await apiFetch<JSONValue[]>("/api/group");

export const getGroup = async (groupId: string): Promise<JSONValue> =>
  await apiFetch<JSONValue>(`/api/group/${groupId}`);

export const updateGroup = async (
  groupId: string,
  data: JSONValue,
): Promise<JSONValue> =>
  apiFetch<JSONValue>(`/api/group/${groupId}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

export const updateGroupParent = async (
  groupId: string,
  parentId: number,
): Promise<JSONValue | null> =>
  apiFetchNullable<JSONValue>(`/api/group/${groupId}/parent/${parentId}`, {
    method: "PUT",
  });

export const removeGroupParent = async (
  groupId: string,
): Promise<JSONValue | null> =>
  apiFetchNullable<JSONValue>(`/api/group/${groupId}/parent`, {
    method: "DELETE",
  });
