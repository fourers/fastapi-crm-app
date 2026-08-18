import { useQuery } from "@tanstack/react-query";

import { ClientTable } from "~/features/clients/ClientTable";
import { type Client } from "~/stores/clientStore";
import { apiFetch } from "~/utils/fetch";

export function Clients() {
  const { data: clients, isLoading } = useQuery({
    queryKey: ["clientsList"],
    queryFn: async () => await apiFetch<Client[]>("/api/client"),
  });

  return <ClientTable clients={clients ?? []} loading={isLoading} />;
}
