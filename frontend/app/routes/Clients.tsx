import { useEffect } from "react";

import { ClientTable } from "~/features/clients/ClientTable";
import { useClientStore } from "~/stores/clientStore";

export function Clients() {
  const clients = useClientStore((state) => state.clients);
  const loading = useClientStore((state) => state.loading);
  const loadClients = useClientStore((state) => state.loadClients);

  useEffect(() => {
    loadClients();
  }, [loadClients]);

  return (
    <>
      <ClientTable clients={clients} loading={loading} />
    </>
  );
}
