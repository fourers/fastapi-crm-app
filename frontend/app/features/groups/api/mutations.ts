import { useMutation, useQueryClient } from "@tanstack/react-query";

import {
  addGroupUser,
  removeGroupParent,
  updateGroup,
  updateGroupParent,
} from "~/features/groups/api/client";
import { groupKeys } from "~/features/groups/api/keys";
import { type GroupInput, type UserSummary } from "~/features/groups/api/types";
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

export const useAddGroupUser = (groupId: string) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ userId }: { userId: string }) =>
      addGroupUser(groupId, userId),

    onSuccess: (data) => {
      if (data) {
        queryClient.setQueryData(
          groupKeys.user(groupId),
          (prev: UserSummary[]) => [...prev, data.user],
        );
      }
      useAppStore.getState().addMessage({
        message: "User was added to group",
        status: Status.success,
      });
    },
  });
};
