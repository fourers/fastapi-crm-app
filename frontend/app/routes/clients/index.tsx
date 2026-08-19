import { useListClients } from "~/features/clients/api/queries";
import { ClientTable } from "~/features/clients/components/ClientTable";

export function Clients() {
  const { data: clients, isLoading } = useListClients();

  return <ClientTable clients={clients ?? []} loading={isLoading} />;
}
