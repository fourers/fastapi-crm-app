import { useEffect } from "react";
import { useForm } from "react-hook-form";

import { useUpdateGroup } from "~/features/groups/api/mutations";
import { useListGroups } from "~/features/groups/api/queries";
import { type Group } from "~/features/groups/api/types";

type GroupInputs = {
  name: string;
  parent_id: string;
};

interface GroupFormProps {
  groupId: string;
  group: Group | undefined;
  isLoading: boolean;
}

export const GroupForm = ({ groupId, group, isLoading }: GroupFormProps) => {
  const { data: groups = [], isLoading: dropdownLoading } = useListGroups();
  const { mutate, isPending } = useUpdateGroup(groupId);

  const { register, handleSubmit, reset, getFieldState, formState } =
    useForm<GroupInputs>({
      defaultValues: {
        name: "",
        parent_id: "",
      },
    });

  const { isDirty: parentChanged } = getFieldState("parent_id", formState);

  useEffect(() => {
    if (group) {
      reset({
        ...group,
        parent_id: group.parent_id === null ? "" : String(group.parent_id),
      } as unknown as GroupInputs);
    }
  }, [group, reset]);

  const onSubmit = (data: GroupInputs) => {
    mutate({
      group: data,
      parentId: data.parent_id ?? "",
      parentChanged: parentChanged,
    });
  };

  const formIsLoading = isLoading || dropdownLoading;

  return (
    <div className="card">
      <div className="card-body">
        <form className="container" onSubmit={handleSubmit(onSubmit)}>
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
