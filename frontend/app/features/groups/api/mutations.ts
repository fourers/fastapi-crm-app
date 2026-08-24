import { useMutation, useQueryClient } from "@tanstack/react-query";

import {
  removeGroupParent,
  updateGroup,
  updateGroupParent,
} from "~/features/groups/api/client";
import { groupKeys } from "~/features/groups/api/keys";
import { Status, useAppStore } from "~/lib/appStore";
import { type JSONValue } from "~/lib/types";

export const useUpdateGroup = (groupId: string) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: JSONValue) => updateGroup(groupId, data),

    onSuccess: (data) => {
      queryClient.setQueryData(groupKeys.detail(groupId), data);
      useAppStore.getState().addMessage({
        message: "Group was updated",
        status: Status.success,
      });
    },
  });
};

export const useUpdateGroupParent = (groupId: string) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (parentId: number | null) =>
      parentId === null
        ? removeGroupParent(groupId)
        : updateGroupParent(groupId, parentId),

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: groupKeys.detail(groupId),
      });
      queryClient.invalidateQueries({
        queryKey: groupKeys.lists(),
      });
    },
  });
};
