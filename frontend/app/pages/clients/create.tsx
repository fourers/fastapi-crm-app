import { useNavigate } from "react-router-dom";

import { Header } from "~/components/Header";
import { CreateClientForm } from "~/features/clients/components/CreateClientForm";
import { headerPaths } from "~/lib/breadcrumbs";

export const CreateClient = () => {
  const navigate = useNavigate();

  return (
    <>
      <Header parents={headerPaths.clients()} currentPage="Create New Client" />
      <CreateClientForm navigate={navigate} />
    </>
  );
};
