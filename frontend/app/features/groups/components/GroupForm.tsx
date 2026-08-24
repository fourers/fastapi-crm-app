import { useEffect } from "react";
import { useForm } from "react-hook-form";

import { useUpdateGroupParent } from "~/features/groups/api/mutations";
import { useListGroups } from "~/features/groups/api/queries";
import type { JSONValue } from "~/lib/types";

interface GroupFormProps {
  group?: JSONValue | null;
  onSubmit: (data: JSONValue) => void;
  loadingForm?: boolean;
  loadingSubmit: boolean;
}

export const GroupForm = ({
  group,
  onSubmit,
  loadingForm = false,
  loadingSubmit,
}: GroupFormProps) => {
  const {
    register,
    handleSubmit,
    reset,
    formState: { isDirty },
  } = useForm({
    defaultValues: {
      name: "",
    },
  });
  const { data: groups = [], isLoading: groupsLoading } = useListGroups();
  const groupId = group?.id?.toString() ?? "";
  const { mutate: updateParent, isPending: parentUpdating } =
    useUpdateGroupParent(groupId);

  useEffect(() => {
    if (group) {
      reset(group);
    }
  }, [group, reset]);

  return (
    <div className="card">
      <div className="card-body">
        <div className="container">
          <label htmlFor="parent_id" className="form-label">
            Parent Group
          </label>

          <select
            id="parent_id"
            className="form-select mb-3"
            value={group?.parent_id?.toString() ?? ""}
            disabled={
              loadingForm || groupsLoading || parentUpdating || !groupId
            }
            onChange={(event) => {
              const value = event.target.value;
              updateParent(value === "" ? null : Number(value));
            }}
          >
            <option value="">{"<No Parent>"}</option>

            {groups
              .filter((candidate) => candidate.id?.toString() !== groupId)
              .map((candidate) => (
                <option
                  key={candidate.id?.toString()}
                  value={candidate.id?.toString()}
                >
                  {candidate.name?.toString() ?? "Unnamed group"}
                </option>
              ))}
          </select>
        </div>
      </div>
      <div className="card-body border-top">
        <form className="container" onSubmit={handleSubmit(onSubmit)}>
          <div className="mb-3">
            <label htmlFor="name" className="form-label">
              Group Name
            </label>
            <input
              {...register("name")}
              id="name"
              className="form-control"
              disabled={loadingForm}
            />
          </div>

          <button
            type="submit"
            className="btn btn-primary"
            disabled={!isDirty || loadingSubmit}
          >
            Save
          </button>
        </form>
      </div>
    </div>
  );
};
