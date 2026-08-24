import { useEffect } from "react";
import { useForm } from "react-hook-form";

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

  useEffect(() => {
    if (group !== null) {
      reset(group);
    }
  }, [group, reset]);

  return (
    <div className="card">
      <div className="card-body">
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
