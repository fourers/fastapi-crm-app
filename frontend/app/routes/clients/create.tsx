import { useNavigate } from "react-router-dom";

import { useCreateClient } from "~/features/clients/api/mutations";
import { CreateClientForm } from "~/features/clients/components/CreateClientForm";
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

  return <CreateClientForm onSubmit={onSubmit} loadingSubmit={isPending} />;
}
