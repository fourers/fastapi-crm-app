import { useEffect } from "react";

import { Table } from "~/features/clients/ClientTable";
import { useClientStore } from "~/stores/clientStore";

export function Clients() {
  const clients = useClientStore((state) => state.clients);
  const loading = useClientStore((state) => state.loading);
  // const error = useClientStore((state) => state.error);
  const loadClient = useClientStore((state) => state.loadClient);

  useEffect(() => {
    loadClient();
  }, [loadClient]);

  return <Table clients={clients} loading={loading} />;
}
