import { Header } from "~/components/Header";
import { Table } from "~/components/Table";
import { useListUsers } from "~/features/users/api/queries";
import { headerPaths } from "~/lib/breadcrumbs";

export const Users = () => {
  const { data: users, isLoading } = useListUsers();

  return (
    <>
      <Header parents={headerPaths.home()} currentPage="Users" />
      <Table
        rows={users ?? []}
        loading={isLoading}
        loadingMessage="Loading users..."
        emptyMessage="No users found."
      />
    </>
  );
};
