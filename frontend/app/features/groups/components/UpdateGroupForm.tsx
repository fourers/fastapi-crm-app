import { useEffect } from "react";
import { useForm } from "react-hook-form";

import { useUpdateGroup } from "~/features/groups/api/mutations";
import { useGetGroup, useListGroups } from "~/features/groups/api/queries";

interface UpdateGroupFormProps {
  groupId: string;
  setHeaderName: (headerName: string) => void;
}

type UpdateGroupInput = {
  name: string;
  parent_id: string;
};

export const UpdateGroupForm = ({
  groupId,
  setHeaderName,
}: UpdateGroupFormProps) => {
  const {
    data: group,
    isLoading: groupLoading,
    isFetched: groupFetched,
  } = useGetGroup(groupId, true);
  const {
    data: groups = [],
    isLoading: dropdownLoading,
    isFetched: dropdownFetched,
  } = useListGroups();
  const { mutate, isPending } = useUpdateGroup(groupId);
  const { register, handleSubmit, reset, getFieldState, formState } =
    useForm<UpdateGroupInput>({
      defaultValues: {
        name: "",
        parent_id: "",
      },
    });

  const { isDirty: parentChanged } = getFieldState("parent_id", formState);

  useEffect(() => {
    if (!group || !dropdownFetched) {
      return;
    }
    reset({
      name: group.name as string,
      parent_id: String(group.parent_id ?? ""),
    });
    setHeaderName(group.name || "Unknown");
  }, [group, dropdownFetched, reset, setHeaderName]);

  const onSubmit = (data: UpdateGroupInput) => {
    mutate({
      group: { name: data.name },
      parentId: data.parent_id,
      parentChanged: parentChanged,
    });
  };

  const formIsLoading =
    groupLoading ||
    dropdownLoading ||
    isPending ||
    !groupFetched ||
    !dropdownFetched;

  return (
    <div className="card">
      <div className="card-body">
        <form className="container" onSubmit={handleSubmit(onSubmit)}>
          <div className="mb-3">
            <label htmlFor="group_name" className="form-label">
              Group Name
            </label>
            <input
              {...register("name")}
              id="group_name"
              className="form-control"
              disabled={formIsLoading}
            />
          </div>

          <div className="mb-3">
            <label htmlFor="parent_id" className="form-label">
              Parent Group
            </label>

            <select
              id="parent_id"
              {...register("parent_id")}
              className="form-select mb-3"
              disabled={formIsLoading}
            >
              <option value="">{"<No Parent>"}</option>

              {groups
                .filter((candidate) => candidate.id.toString() !== groupId)
                .map((candidate) => (
                  <option key={candidate.id} value={candidate.id}>
                    {candidate.name ?? "Unnamed group"}
                  </option>
                ))}
            </select>
          </div>

          <button
            type="submit"
            className="btn btn-primary"
            disabled={!formState.isDirty || formIsLoading || isPending}
          >
            Save
          </button>
        </form>
      </div>
    </div>
  );
};
