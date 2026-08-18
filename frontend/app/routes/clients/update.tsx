import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Navigate, useParams } from "react-router-dom";

import { CreateClientForm } from "~/features/clients/CreateClientForm";
import { Status, useAppStore } from "~/stores/appStore";
import { apiFetch } from "~/utils/fetch";
import type { JSONValue } from "~/utils/types";

async function getClient(clientId: string): Promise<JSONValue> {
  return apiFetch<JSONValue>(`/api/client/${clientId}`);
}

function useClient(clientId: string | undefined, enabled: boolean) {
  return useQuery({
    queryKey: ["client", clientId],
    queryFn: () => getClient(clientId ?? ""),
    enabled: enabled,
  });
}

async function updateClient(clientId: string, data: JSONValue) {
  return await apiFetch<JSONValue>(`/api/client/${clientId}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
}

function useUpdateClient(clientId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: JSONValue) => updateClient(clientId, data),

    onSuccess: (updatedClient) => {
      queryClient.setQueryData(["client", clientId], updatedClient);
      useAppStore.getState().addMessage({
        message: "Successfully updated client",
        status: Status.success,
      });
    },
  });
}

export function UpdateClient() {
  const { id: clientId } = useParams<{ id: string }>();

  const {
    data: client,
    isLoading: formIsLoading,
    error: formError,
  } = useClient(clientId, Number.isInteger(Number(clientId)));
  const { mutate, isPending: submitIsLoading } = useUpdateClient(clientId!);

  if (!Number.isInteger(Number(clientId))) {
    return <Navigate to="/clients" />;
  }

  return (
    <CreateClientForm
      client={client}
      onSubmit={async (data) => mutate(data)}
      loadingForm={formIsLoading || (!!formError && !client)}
      loadingSubmit={submitIsLoading}
    />
  );
}
