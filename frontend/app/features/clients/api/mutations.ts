import { useMutation, useQueryClient } from "@tanstack/react-query";

import { createClient, updateClient } from "~/features/clients/api/client";
import { clientKeys } from "~/features/clients/api/keys";
import { type ClientInput } from "~/features/clients/api/types";
import { Status, useAppStore } from "~/lib/appStore";

export const useCreateClient = () =>
  useMutation({
    mutationFn: (data: ClientInput) => createClient(data),

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
    mutationFn: (data: ClientInput) => updateClient(clientId, data),

    onSuccess: (data) => {
      queryClient.setQueryData(clientKeys.detail(clientId), data);
      useAppStore.getState().addMessage({
        message: "Client was updated",
        status: Status.success,
      });
    },
  });
};
