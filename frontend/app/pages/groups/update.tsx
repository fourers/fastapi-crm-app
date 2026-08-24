import { Navigate, useParams } from "react-router-dom";

import { Header } from "~/components/Header";
import { useUpdateGroup } from "~/features/groups/api/mutations";
import { useGetGroup } from "~/features/groups/api/queries";
import { GroupForm } from "~/features/groups/components/GroupForm";
import { headerPaths } from "~/lib/breadcrumbs";

const isPositiveInteger = (value: string | undefined): boolean => {
  const numberValue = Number(value);
  return Number.isInteger(numberValue) && numberValue > 0;
};

export const UpdateGroup = () => {
  const { id } = useParams<{ id: string }>();
  const validId = isPositiveInteger(id);
  const {
    data,
    isLoading: formIsLoading,
    error: formError,
  } = useGetGroup(id!, validId);
  const { mutate, isPending: submitIsLoading } = useUpdateGroup(id!);

  if (!validId) {
    return <Navigate to="/groups" />;
  }

  return (
    <>
      <Header
        parents={headerPaths.groups()}
        currentPage={data?.name?.toString() ?? "Unknown"}
      />
      <GroupForm
        group={data}
        onSubmit={async (data) => mutate(data)}
        loadingForm={formIsLoading || (!!formError && !data)}
        loadingSubmit={submitIsLoading}
      />
    </>
  );
};
