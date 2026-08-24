import { useMutation, useQueryClient } from "@tanstack/react-query";

import { updateGroup } from "~/features/groups/api/client";
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
