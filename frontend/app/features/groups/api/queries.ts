import { useQuery } from "@tanstack/react-query";

import { listGroups } from "~/features/groups/api/client";
import { groupKeys } from "~/features/groups/api/keys";

export const useListGroups = () =>
  useQuery({
    queryKey: groupKeys.lists(),
    queryFn: () => listGroups(),
  });
