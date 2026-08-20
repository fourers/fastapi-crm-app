import "bootstrap/dist/css/bootstrap.min.css";
import "~/app.css";

import { QueryClientProvider } from "@tanstack/react-query";
import { redirect } from "react-router";
import {
  createBrowserRouter,
  type LoaderFunctionArgs,
  RouterProvider,
} from "react-router-dom";

import { ErrorScreen } from "~/components/ErrorScreen";
import { AppLayout } from "~/layouts/AppLayout";
import { PublicLayout } from "~/layouts/PublicLayout";
import { Home } from "~/routes";
import { NotFound } from "~/routes/404";
import { Clients } from "~/routes/clients";
import { CreateClient } from "~/routes/clients/create";
import { UpdateClient } from "~/routes/clients/update";
import { Login } from "~/routes/login";
import { Users } from "~/routes/users";
import { getSessionQuery } from "~/utils/auth";
import { queryClient } from "~/utils/queryClient";
import { ApiError, AuthError } from "~/utils/types";

const loginLoader = async () => {
  try {
    const response = await fetch("/auth/me", {
      credentials: "include",
    });

    if (response.ok) {
      return redirect("/");
    }
  } catch {
    // Do nothing
  }
};

const authLoader = async ({ url }: LoaderFunctionArgs) => {
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

const App = () => {
  const router = createBrowserRouter([
    {
      element: <PublicLayout />,
      loader: loginLoader,
      HydrateFallback: () => null,
      children: [
        {
          path: "/login",
          element: <Login />,
        },
      ],
    },
    {
      element: <AppLayout />,
      loader: authLoader,
      errorElement: <ErrorScreen />,
      HydrateFallback: () => null,
      children: [
        {
          path: "/",
          element: <Home />,
        },
        {
          path: "/clients",
          element: <Clients />,
        },
        {
          path: "/clients/:id",
          element: <UpdateClient />,
        },
        {
          path: "clients/create",
          element: <CreateClient />,
        },
        {
          path: "/users",
          element: <Users />,
        },
        {
          path: "*",
          element: <NotFound />,
        },
      ],
    },
  ]);

  return (
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  );
};

export default App;
