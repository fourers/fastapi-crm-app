import { useMutation, useQueryClient } from "@tanstack/react-query";

import {
  removeGroupParent,
  updateGroup,
  updateGroupParent,
} from "~/features/groups/api/client";
import { groupKeys } from "~/features/groups/api/keys";
import { type GroupInput } from "~/features/groups/api/types";
import { Status, useAppStore } from "~/lib/appStore";

export const useUpdateGroup = (groupId: string) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({
      group,
      parentId,
      parentChanged,
    }: {
      group: GroupInput;
      parentId: string;
      parentChanged: boolean;
    }) => {
      if (parentChanged) {
        if (parentId === "") {
          await removeGroupParent(groupId);
        } else {
          await updateGroupParent(groupId, parentId);
        }
      }

      return updateGroup(groupId, group);
    },

    onSuccess: (data) => {
      queryClient.setQueryData(groupKeys.detail(groupId), data);
      useAppStore.getState().addMessage({
        message: "Group was updated",
        status: Status.success,
      });
    },
  });
};
