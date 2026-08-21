import { useEffect } from "react";
import { useForm } from "react-hook-form";

import type { JSONValue } from "~/lib/types";

interface ClientFormProps {
  client?: JSONValue | null;
  onSubmit: (data: JSONValue) => void;
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
    register,
    handleSubmit,
    reset,
    formState: { isDirty },
  } = useForm({
    defaultValues: {
      first_name: "",
      last_name: "",
      email: "",
    },
  });

  useEffect(() => {
    if (client !== null) {
      reset(client);
    }
  }, [client, reset]);

  return (
    <div className="card">
      <div className="card-body">
        <form className="container" onSubmit={handleSubmit(onSubmit)}>
          <div className="mb-3">
            <label htmlFor="firstName" className="form-label">
              First Name
            </label>
            <input
              {...register("first_name")}
              id="firstName"
              className="form-control"
              disabled={loadingForm}
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
              disabled={loadingForm}
            />
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
