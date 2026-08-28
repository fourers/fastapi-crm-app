import { type Client, type ClientInput } from "~/features/clients/api/types";
import { apiFetch, apiFetchNullable } from "~/lib/fetch";
import { type JSONValue } from "~/lib/types";

export const listClients = async (): Promise<Client[]> =>
  await apiFetch<Client[]>("/api/client");

export const getClient = async (clientId: string): Promise<JSONValue> =>
  await apiFetch<JSONValue>(`/api/client/${clientId}`);

export const createClient = async (data: ClientInput): Promise<JSONValue> =>
  await apiFetch<JSONValue>("/api/client", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

export const updateClient = async (
  clientId: string,
  data: ClientInput,
): Promise<JSONValue> =>
  apiFetch<JSONValue>(`/api/client/${clientId}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

export const updateClientOwner = async (
  clientId: string,
  ownerId: string,
): Promise<JSONValue | null> =>
  apiFetchNullable<JSONValue>(`/api/client/${clientId}/owner/${ownerId}`, {
    method: "PUT",
  });
