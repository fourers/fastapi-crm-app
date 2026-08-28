import { useForm } from "react-hook-form";
import { type NavigateFunction } from "react-router-dom";

import { useCreateClient } from "~/features/clients/api/mutations";

interface CreateClientFormProps {
  navigate: NavigateFunction;
}

type CreateClientFormInput = {
  first_name: string;
  last_name: string;
  email: string;
};

export const CreateClientForm = ({ navigate }: CreateClientFormProps) => {
  const { register, handleSubmit, formState } = useForm<CreateClientFormInput>({
    defaultValues: {
      first_name: "",
      last_name: "",
      email: "",
    },
  });
  const { mutate, isPending } = useCreateClient();

  const onSubmit = (data: CreateClientFormInput) =>
    mutate(data, {
      onSuccess: (response) => {
        navigate(`/clients/${response.id}`);
      },
    });

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
              disabled={isPending}
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
              disabled={isPending}
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
              disabled={isPending}
            />
          </div>

          <button
            type="submit"
            className="btn btn-primary"
            disabled={!formState.isDirty || isPending}
          >
            Save
          </button>
        </form>
      </div>
    </div>
  );
};
