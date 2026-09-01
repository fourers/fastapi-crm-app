import { GenericTable } from "~/components/GenericTable";
import { useListSubgroups } from "~/features/groups/api/queries";
import type { JSONValue } from "~/lib/types";

type GroupSubGroupTableProps = {
  groupId: string;
};

export const GroupSubGroupTable = ({ groupId }: GroupSubGroupTableProps) => {
  const { data, isLoading } = useListSubgroups(groupId);

  return (
    <div className="card">
      <div className="card-body">
        <div className="container">
          <GenericTable
            rows={(data as unknown as JSONValue[]) ?? []}
            loading={isLoading}
            loadingMessage="Loading subgroups..."
            emptyMessage="No subgroups found."
          />
        </div>
      </div>
    </div>
  );
};
