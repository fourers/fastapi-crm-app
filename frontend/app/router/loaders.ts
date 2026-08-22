import { redirect } from "react-router";
import { type LoaderFunctionArgs } from "react-router-dom";

import {
  getSessionAlwaysQuery,
  getSessionQuery,
  type UserSession,
} from "~/lib/auth";
import { queryClient } from "~/lib/queryClient";
import { ApiError, AuthError } from "~/lib/types";

export const loginLoader = async (): Promise<Response | undefined> => {
  try {
    await queryClient.ensureQueryData(getSessionAlwaysQuery());
    return redirect("/");
  } catch {
    // Do nothing
  }
};

export const authLoader = async ({
  url,
}: LoaderFunctionArgs): Promise<UserSession | Response> => {
  try {
    return await queryClient.ensureQueryData(getSessionQuery());
  } catch (error) {
    if (error instanceof ApiError && error.status === 401) {
      if (url.pathname === "/") {
        return redirect("/login");
      } else {
        return redirect(
          `/login?next=${encodeURIComponent(`${url.pathname}${url.search}${url.hash}`)}`,
        );
      }
    }
    if (error instanceof ApiError) {
      throw error;
    } else {
      throw new AuthError("Failed to check authentication");
    }
  }
};
