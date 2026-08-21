import { useMutation, useQueryClient } from "@tanstack/react-query";

import { createClient, updateClient } from "~/features/clients/api/client";
import { clientKeys } from "~/features/clients/api/keys";
import { Status, useAppStore } from "~/lib/appStore";
import { type JSONValue } from "~/lib/types";

export const useCreateClient = () =>
  useMutation({
    mutationFn: (data: JSONValue) => createClient(data),

    onSuccess: () => {
      useAppStore.getState().addMessage({
        message: "New client was created",
        status: Status.success,
      });
    },
  });

export const useUpdateClient = (clientId: string) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: JSONValue) => updateClient(clientId, data),

    onSuccess: (data) => {
      queryClient.setQueryData(clientKeys.detail(clientId), data);
      useAppStore.getState().addMessage({
        message: "Client was updated",
        status: Status.success,
      });
    },
  });
};
