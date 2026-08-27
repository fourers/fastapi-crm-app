import { Navigate, useParams } from "react-router-dom";

import { Header } from "~/components/Header";
import { useGetGroup } from "~/features/groups/api/queries";
import { GroupForm } from "~/features/groups/components/GroupForm";
import { GroupUserTable } from "~/features/groups/components/GroupUserTable";
import { headerPaths } from "~/lib/breadcrumbs";

const isPositiveInteger = (value: string | undefined): boolean => {
  const numberValue = Number(value);
  return Number.isInteger(numberValue) && numberValue > 0;
};

export const UpdateGroup = () => {
  const { id } = useParams<{ id: string }>();
  const isValid = isPositiveInteger(id);
  const { data: group, isLoading, error } = useGetGroup(id!, isValid);

  if (!isPositiveInteger(id)) {
    return <Navigate to="/groups" />;
  }

  return (
    <>
      <Header
        parents={headerPaths.groups()}
        currentPage={group?.name?.toString() ?? "Unknown"}
      />
      <GroupForm
        groupId={id!}
        group={group}
        isLoading={isLoading || (!!error && !group)}
      />
      <div className="mt-4">
        <p className="fs-5 fw-light">Users</p>
        <GroupUserTable groupId={id!} />
      </div>
    </>
  );
};
