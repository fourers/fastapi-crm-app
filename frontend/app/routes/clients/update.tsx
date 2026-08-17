import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import { CreateClientForm } from "~/features/clients/CreateClientForm";
import { Status, useAppStore } from "~/stores/appStore";
import { apiFetch } from "~/utils/fetch";
import type { JSONValue } from "~/utils/types";

export function UpdateClient() {
  const params = useParams();
  const navigate = useNavigate();
  const [loadingForm, setLoadingForm] = useState(false);
  const [client, setClient] = useState<JSONValue | null>(null);
  const [loadingSubmit, setLoadingSubmit] = useState(false);

  const clientId = Number.parseInt(params.id || "");

  const loadForm = async () => {
    setLoadingForm(true);
    if (!Number.isInteger(clientId)) {
      throw navigate("/clients");
    }

    const response = await apiFetch<JSONValue>(`/api/client/${clientId}`);

    setLoadingForm(false);
    if (response === null) {
      throw navigate("/clients");
    }
    setClient(response);
  };

  useEffect(() => {
    loadForm();
  }, [params]); // eslint-disable-line react-hooks/exhaustive-deps

  const onSubmit = async (data: JSONValue) => {
    setLoadingSubmit(true);
    const response = await apiFetch<JSONValue>(`/api/client/${clientId}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    setLoadingSubmit(false);
    if (response !== null) {
      setClient(response);
      useAppStore.getState().addMessage({
        message: "Successfully updated client",
        status: Status.success,
      });
    }
  };
  return (
    <CreateClientForm
      client={client}
      onSubmit={onSubmit}
      loadingForm={loadingForm}
      loadingSubmit={loadingSubmit}
    />
  );
}
