import { useEffect } from "react";

import { ErrorToast } from "~/components/ErrorToast";
import { ClientTable } from "~/features/clients/ClientTable";
import { useClientStore } from "~/stores/clientStore";

export function Clients() {
  const clients = useClientStore((state) => state.clients);
  const loading = useClientStore((state) => state.loading);
  const error = useClientStore((state) => state.error);
  const loadClients = useClientStore((state) => state.loadClients);

  useEffect(() => {
    loadClients();
  }, [loadClients]);

  return (
    <>
      <ErrorToast error={error} />
      <ClientTable clients={clients} loading={loading} />
    </>
  );
}
