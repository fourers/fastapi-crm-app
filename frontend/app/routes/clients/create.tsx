import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { CreateClientForm } from "~/features/clients/CreateClientForm";
import { apiFetch } from "~/utils/fetch";
import type { JSONValue } from "~/utils/types";

export function CreateClient() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const onSubmit = async (data: JSONValue) => {
    setLoading(true);
    const response = await apiFetch("/api/client", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    setLoading(false);
    if (response !== null) {
      throw navigate("/clients");
    }
  };
  return <CreateClientForm onSubmit={onSubmit} loadingSubmit={loading} />;
}
