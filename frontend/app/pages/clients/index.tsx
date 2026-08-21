import { Link } from "react-router-dom";

import { Header } from "~/components/Header";
import { useListClients } from "~/features/clients/api/queries";
import { ClientTable } from "~/features/clients/components/ClientTable";
import { headerPaths } from "~/lib/breadcrumbs";

export const Clients = () => {
  const { data: clients, isLoading } = useListClients();

  return (
    <>
      <div className="row">
        <div className="col">
          <Header parents={headerPaths.home()} currentPage="Clients" />
        </div>
        <div className="col-md-auto">
          <Link to="/clients/create">New Client</Link>
        </div>
      </div>

      <ClientTable clients={clients ?? []} loading={isLoading} />
    </>
  );
};
