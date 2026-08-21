import { Header } from "~/components/Header";
import { useListClients } from "~/features/clients/api/queries";
import { ClientTable } from "~/features/clients/components/ClientTable";
import { headerPaths } from "~/lib/breadcrumbs";

export const Clients = () => {
  const { data: clients, isLoading } = useListClients();

  return (
    <>
      <Header parents={headerPaths.home()} currentPage="Clients" />
      <ClientTable clients={clients ?? []} loading={isLoading} />
    </>
  );
};
