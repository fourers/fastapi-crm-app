import { GenericTable } from "~/components/GenericTable";
import { useListGroupUsers } from "~/features/groups/api/queries";
import type { JSONValue } from "~/lib/types";

type GroupUserTableProps = {
  groupId: string;
};

export const GroupUserTable = ({ groupId }: GroupUserTableProps) => {
  const { data, isLoading } = useListGroupUsers(groupId);

  return (
    <div className="card">
      <div className="card-body">
        <div className="container">
          <GenericTable
            rows={(data as unknown as JSONValue[]) ?? []}
            loading={isLoading}
            loadingMessage="Loading group users..."
            emptyMessage="No users found."
          />
        </div>
      </div>
    </div>
  );
};
