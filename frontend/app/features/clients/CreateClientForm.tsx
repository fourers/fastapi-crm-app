import { useForm } from "react-hook-form";

import type { JSONValue } from "~/utils/types";

interface CreateClientFormProps {
  onSubmit: (data: JSONValue) => Promise<void>;
  loading: boolean;
}

export function CreateClientForm({ onSubmit, loading }: CreateClientFormProps) {
  const {
    register,
    handleSubmit,
    formState: { isDirty },
  } = useForm({
    defaultValues: {
      first_name: "",
      last_name: "",
      email: "",
    },
  });

  return (
    <form className="container mt-4" onSubmit={handleSubmit(onSubmit)}>
      <div className="mb-3">
        <label htmlFor="firstName" className="form-label">
          First Name
        </label>
        <input {...register("first_name")} id="firstName" className="form-control" />
      </div>

      <div className="mb-3">
        <label htmlFor="lastName" className="form-label">
          Last Name
        </label>
        <input {...register("last_name")} id="lastName" className="form-control" />
      </div>

      <div className="mb-3">
        <label htmlFor="email" className="form-label">
          Email
        </label>
        <input {...register("email")} id="email" type="email" className="form-control" />
      </div>

      <button type="submit" className="btn btn-primary" disabled={!isDirty || loading}>
        Save
      </button>
    </form>
  );
}
