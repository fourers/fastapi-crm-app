import { useEffect } from "react";
import { useForm } from "react-hook-form";

import { useUpdateClient } from "~/features/clients/api/mutations";
import { useGetClient } from "~/features/clients/api/queries";
import { useListUsers } from "~/features/users/api/queries";
import { formatName } from "~/lib/formatters";

interface UpdateClientFormProps {
  clientId: string;
  setHeaderName: (headerName: string) => void;
}

type UpdateClientFormInput = {
  first_name: string;
  last_name: string;
  email: string;
  owner_id: string;
};

export const UpdateClientForm = ({
  clientId,
  setHeaderName,
}: UpdateClientFormProps) => {
  const {
    data: client,
    isLoading: clientLoading,
    error: clientError,
  } = useGetClient(clientId, true);
  const { mutate, isPending } = useUpdateClient(clientId);
  const {
    data: users,
    isLoading: dropdownLoading,
    isFetched: dropdownFetched,
  } = useListUsers();
  const { register, handleSubmit, reset, getFieldState, formState } =
    useForm<UpdateClientFormInput>({
      defaultValues: {
        first_name: "",
        last_name: "",
        email: "",
        owner_id: "",
      },
    });

  const { isDirty: ownerChanged } = getFieldState("owner_id", formState);

  useEffect(() => {
    if (!client || !dropdownFetched) {
      return;
    }
    reset({
      first_name: client.first_name as string,
      last_name: client.last_name as string,
      email: client.email as string,
      owner_id: String(client.owner_id ?? ""),
    });
    setHeaderName(formatName(client));
  }, [client, dropdownFetched, reset, setHeaderName]);

  const onSubmit = (data: UpdateClientFormInput) => {
    mutate({
      data: {
        first_name: data.first_name,
        last_name: data.last_name,
        email: data.email,
      },
      ownerId: data.owner_id,
      ownerChanged: ownerChanged,
    });
  };

  const formIsLoading =
    clientLoading || dropdownLoading || isPending || (!!clientError && !client);

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
            disabled={!formState.isDirty || isPending}
          >
            Save
          </button>
        </form>
      </div>
    </div>
  );
};
