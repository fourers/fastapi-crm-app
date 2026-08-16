import { useNavigate } from "react-router-dom";

import { CreateClientForm } from "~/features/clients/CreateClientForm";
import { apiFetch } from "~/utils/fetch";
import type { JSONValue } from "~/utils/types";

export function CreateClient() {
  const navigate = useNavigate();

  const onSubmit = async (data: JSONValue) => {
    const response = await apiFetch("/api/client", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data),
    });

    if (response !== null) {
      throw navigate("/clients");
    }
  };
  return <CreateClientForm onSubmit={onSubmit} />;
}
