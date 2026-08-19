import { Navigate, useParams } from "react-router-dom";

import { useUpdateClient } from "~/features/clients/api/mutations";
import { useGetClient } from "~/features/clients/api/queries";
import { CreateClientForm } from "~/features/clients/components/CreateClientForm";

export function UpdateClient() {
  const { id: clientId } = useParams<{ id: string }>();
  const validClientId = Number.isInteger(Number(clientId));
  const {
    data: client,
    isLoading: formIsLoading,
    error: formError,
  } = useGetClient(clientId!, validClientId);
  const { mutate, isPending: submitIsLoading } = useUpdateClient(clientId!);

  if (!validClientId) {
    return <Navigate to="/clients" />;
  }

  return (
    <CreateClientForm
      client={client}
      onSubmit={async (data) => mutate(data)}
      loadingForm={formIsLoading || (!!formError && !client)}
      loadingSubmit={submitIsLoading}
    />
  );
}
