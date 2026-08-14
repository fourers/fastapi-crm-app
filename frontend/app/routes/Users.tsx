import { useEffect } from "react";

import { Table } from "~/components/Table";
import { useUserStore } from "~/stores/userStore";

export function Users() {
  const users = useUserStore((state) => state.data);
  const loading = useUserStore((state) => state.loading);
  const loadUsers = useUserStore((state) => state.loadData);

  useEffect(() => {
    loadUsers();
  }, [loadUsers]);

  return (
    <>
      <Table
        rows={users}
        loading={loading}
        title="Users"
        loadingMessage="Loading users..."
        emptyMessage="No users found."
      />
    </>
  );
}
