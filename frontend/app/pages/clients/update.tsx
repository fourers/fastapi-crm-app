import { useState } from "react";
import { Navigate, useParams } from "react-router-dom";

import { Header } from "~/components/Header";
import { UpdateClientForm } from "~/features/clients/components/UpdateClientForm";
import { headerPaths } from "~/lib/breadcrumbs";

const isPositiveInteger = (value: string | undefined): boolean => {
  const numberValue = Number(value);
  return Number.isInteger(numberValue) && numberValue > 0;
};

export const UpdateClient = () => {
  const { id: clientId } = useParams<{ id: string }>();
  const validClientId = isPositiveInteger(clientId);
  const [headerName, setHeaderName] = useState("");

  if (!validClientId) {
    return <Navigate to="/clients" />;
  }

  return (
    <>
      <Header parents={headerPaths.clients()} currentPage={headerName} />
      <UpdateClientForm clientId={clientId!} setHeaderName={setHeaderName} />
    </>
  );
};
