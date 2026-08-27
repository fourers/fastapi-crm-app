import { useQuery } from "@tanstack/react-query";

import {
  getGroup,
  listGroups,
  listGroupUsers,
} from "~/features/groups/api/client";
import { groupKeys } from "~/features/groups/api/keys";

export const useListGroups = () =>
  useQuery({
    queryKey: groupKeys.lists(),
    queryFn: () => listGroups(),
  });

export const useGetGroup = (groupId: string, enabled: boolean) =>
  useQuery({
    queryKey: groupKeys.detail(groupId),
    queryFn: () => getGroup(groupId),
    enabled: enabled,
  });

export const useListGroupUsers = (groupId: string) =>
  useQuery({
    queryKey: groupKeys.user(groupId),
    queryFn: () => listGroupUsers(groupId),
  });
