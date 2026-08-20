import { useNavigate } from "react-router-dom";

import { Header } from "~/components/Header";
import { useCreateClient } from "~/features/clients/api/mutations";
import { ClientForm } from "~/features/clients/components/ClientForm";
import { headerPaths } from "~/utils/breadcrumbs";
import type { JSONValue } from "~/utils/types";

export function CreateClient() {
  const navigate = useNavigate();
  const { mutate, isPending } = useCreateClient();

  const onSubmit = (data: JSONValue) =>
    mutate(data, {
      onSuccess: (data) => {
        navigate(`/clients/${data.id}`);
      },
    });

  return (
    <>
      <Header parents={headerPaths.clients()} currentPage="<Create>" />
      <ClientForm onSubmit={onSubmit} loadingSubmit={isPending} />
    </>
  );
}
