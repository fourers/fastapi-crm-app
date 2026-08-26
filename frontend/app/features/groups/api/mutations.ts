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
    mutationFn: async ({
      group,
      parentId,
      parentChanged,
    }: {
      group: JSONValue;
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
