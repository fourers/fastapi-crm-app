import { Header } from "~/components/Header";
import { Table } from "~/components/Table";
import { useListGroups } from "~/features/groups/api/queries";
import { headerPaths } from "~/lib/breadcrumbs";

export const Groups = () => {
  const { data, isLoading } = useListGroups();

  return (
    <>
      <Header parents={headerPaths.home()} currentPage="Groups" />
      <Table
        rows={data ?? []}
        loading={isLoading}
        loadingMessage="Loading groups..."
        emptyMessage="No groups found."
      />
    </>
  );
};
