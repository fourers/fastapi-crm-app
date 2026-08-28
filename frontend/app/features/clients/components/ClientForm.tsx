import { useEffect } from "react";
import { useForm } from "react-hook-form";

import { useListUsers } from "~/features/users/api/queries";
import { formatName } from "~/lib/formatters";
import type { JSONValue } from "~/lib/types";

interface ClientFormProps {
  client?: JSONValue | null;
  onSubmit: (data: JSONValue, ownerChanged: boolean) => void;
  loadingForm?: boolean;
  loadingSubmit: boolean;
}

export const ClientForm = ({
  client,
  onSubmit,
  loadingForm = false,
  loadingSubmit,
}: ClientFormProps) => {
  const {
    data: users,
    isLoading: dropdownLoading,
    isFetched: dropdownFetched,
  } = useListUsers();
  const { register, handleSubmit, reset, getFieldState, formState } = useForm({
    defaultValues: {
      first_name: "",
      last_name: "",
      email: "",
      owner_id: "",
    },
  });

  const formIsLoading = loadingForm || dropdownLoading;

  const { isDirty: ownerChanged } = getFieldState("owner_id", formState);

  const submitForm = (data: JSONValue) => {
    onSubmit(data, ownerChanged);
  };

  useEffect(() => {
    if (!client || !dropdownFetched) {
      return;
    }
    reset({
      ...client,
      owner_id: String(client.owner_id ?? ""),
    });
  }, [client, dropdownFetched, reset]);

  return (
    <div className="card">
      <div className="card-body">
        <form className="container" onSubmit={handleSubmit(submitForm)}>
          <div className="mb-3">
            <label htmlFor="firstName" className="form-label">
              First Name
            </label>
            <input
              {...register("first_name")}
              id="firstName"
              className="form-control"
              disabled={formIsLoading}
            />
          </div>

          <div className="mb-3">
            <label htmlFor="lastName" className="form-label">
              Last Name
            </label>
            <input
              {...register("last_name")}
              id="lastName"
              className="form-control"
              disabled={formIsLoading}
            />
          </div>

          <div className="mb-3">
            <label htmlFor="owner_id" className="form-label">
              Owner
            </label>

            <select
              id="owner_id"
              {...register("owner_id")}
              className="form-select mb-3"
              disabled={formIsLoading}
            >
              {(users ?? []).map((candidate) => (
                <option key={candidate.id} value={candidate.id!.toString()}>
                  {formatName(candidate)}
                </option>
              ))}
            </select>
          </div>

          <div className="mb-3">
            <label htmlFor="email" className="form-label">
              Email
            </label>
            <input
              {...register("email")}
              id="email"
              type="email"
              className="form-control"
              disabled={formIsLoading}
            />
          </div>

          <button
            type="submit"
            className="btn btn-primary"
            disabled={!formState.isDirty || loadingSubmit}
          >
            Save
          </button>
        </form>
      </div>
    </div>
  );
};
