import { useQuery } from "@tanstack/react-query";

import { getClient, listClients } from "~/features/clients/api/client";
import { clientKeys } from "~/features/clients/api/keys";

export const useListClients = () =>
  useQuery({
    queryKey: clientKeys.lists(),
    queryFn: () => listClients(),
  });

export const useGetClient = (clientId: string, enabled: boolean) =>
  useQuery({
    queryKey: clientKeys.detail(clientId),
    queryFn: () => getClient(clientId),
    enabled: enabled,
  });
