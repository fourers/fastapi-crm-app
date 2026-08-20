import { queryOptions } from "@tanstack/react-query";

import { apiFetch } from "~/utils/fetch";

interface UserSession {
  id: number;
  username: string;
}

const authKeys = ["auth", "me"];

export const getSession = async (): Promise<UserSession> => {
  return await apiFetch<UserSession>("/auth/me");
};

export const getSessionQuery = () =>
  queryOptions({
    queryKey: authKeys,
    queryFn: () => getSession(),
    staleTime: 5 * 60 * 1000,
  });

export const getSessionAlwaysQuery = () =>
  queryOptions({
    queryKey: ["auth", "me"],
    queryFn: () => getSession(),
    staleTime: 0,
    gcTime: 0,
    refetchOnMount: true,
  });
