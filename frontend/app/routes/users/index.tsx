import { Table } from "~/components/Table";
import { useListUsers } from "~/features/users/api/queries";

export function Users() {
  const { data: users, isLoading } = useListUsers();

  return (
    <>
      <Table
        rows={users ?? []}
        loading={isLoading}
        title="Users"
        loadingMessage="Loading users..."
        emptyMessage="No users found."
      />
    </>
  );
}
