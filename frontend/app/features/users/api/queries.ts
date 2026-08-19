import { useQuery } from "@tanstack/react-query";

import { listUsers } from "~/features/users/api/client";
import { userKeys } from "~/features/users/api/keys";

export const useListUsers = () =>
  useQuery({
    queryKey: userKeys.lists(),
    queryFn: () => listUsers(),
  });
