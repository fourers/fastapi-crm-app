import { Navigate, useParams } from "react-router-dom";

import { Header } from "~/components/Header";
import { useUpdateClient } from "~/features/clients/api/mutations";
import { useGetClient } from "~/features/clients/api/queries";
import { ClientForm } from "~/features/clients/components/ClientForm";
import { headerPaths } from "~/lib/breadcrumbs";
import { formatName } from "~/lib/formatters";

const isPositiveInteger = (value: string | undefined): boolean => {
  const numberValue = Number(value);
  return Number.isInteger(numberValue) && numberValue > 0;
};

export const UpdateClient = () => {
  const { id: clientId } = useParams<{ id: string }>();
  const validClientId = isPositiveInteger(clientId);
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
    <>
      <Header
        parents={headerPaths.clients()}
        currentPage={formatName(client)}
      />
      <ClientForm
        client={client}
        onSubmit={async (data) => mutate(data)}
        loadingForm={formIsLoading || (!!formError && !client)}
        loadingSubmit={submitIsLoading}
      />
    </>
  );
};
