import { useState } from "react";
import { Navigate, useParams } from "react-router-dom";

import { Header } from "~/components/Header";
import { GroupSubGroupTable } from "~/features/groups/components/GroupSubgroupTable";
import { GroupUserTable } from "~/features/groups/components/GroupUserTable";
import { UpdateGroupForm } from "~/features/groups/components/UpdateGroupForm";
import { headerPaths } from "~/lib/breadcrumbs";

const isPositiveInteger = (value: string | undefined): boolean => {
  const numberValue = Number(value);
  return Number.isInteger(numberValue) && numberValue > 0;
};

export const UpdateGroup = () => {
  const { id } = useParams<{ id: string }>();
  const [headerName, setHeaderName] = useState("");

  if (!isPositiveInteger(id)) {
    return <Navigate to="/groups" />;
  }

  return (
    <>
      <Header parents={headerPaths.groups()} currentPage={headerName} />
      <UpdateGroupForm groupId={id!} setHeaderName={setHeaderName} />
      <div className="mt-4">
        <p className="fs-5 fw-light">Subgroups</p>
        <GroupSubGroupTable groupId={id!} />
      </div>
      <div className="mt-4">
        <p className="fs-5 fw-light">Users</p>
        <GroupUserTable groupId={id!} />
      </div>
    </>
  );
};
