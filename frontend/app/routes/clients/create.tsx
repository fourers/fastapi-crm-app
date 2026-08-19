import { useNavigate } from "react-router-dom";

import { useCreateClient } from "~/features/clients/api/mutations";
import { ClientForm } from "~/features/clients/components/ClientForm";
import { ClientHeader } from "~/features/clients/components/ClientHeader";
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
      <ClientHeader sectionName="Create" />
      <ClientForm onSubmit={onSubmit} loadingSubmit={isPending} />
    </>
  );
}
