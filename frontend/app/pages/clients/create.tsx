import { useNavigate } from "react-router-dom";

import { Header } from "~/components/Header";
import { useCreateClient } from "~/features/clients/api/mutations";
import { ClientForm } from "~/features/clients/components/ClientForm";
import { headerPaths } from "~/lib/breadcrumbs";
import type { JSONValue } from "~/lib/types";

export const CreateClient = () => {
  const navigate = useNavigate();
  const { mutate, isPending } = useCreateClient();

  const onSubmit = (data: JSONValue) =>
    mutate(
      {
        first_name: data.first_name as string,
        last_name: data.last_name as string,
        email: data.email as string,
      },
      {
        onSuccess: (response) => {
          navigate(`/clients/${response.id}`);
        },
      },
    );

  return (
    <>
      <Header parents={headerPaths.clients()} currentPage="Create New Client" />
      <ClientForm onSubmit={onSubmit} loadingSubmit={isPending} />
    </>
  );
};
