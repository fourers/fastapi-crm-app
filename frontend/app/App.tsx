import "bootstrap/dist/css/bootstrap.min.css";
import "~/app.css";

import { redirect } from "react-router";
import { createBrowserRouter, type LoaderFunctionArgs, RouterProvider } from "react-router-dom";

import { ErrorScreen } from "~/components/ErrorScreen";
import { AppLayout } from "~/layouts/AppLayout";
import { PublicLayout } from "~/layouts/PublicLayout";
import { Home } from "~/routes";
import { NotFound } from "~/routes/404";
import { Clients } from "~/routes/clients";
import { Login } from "~/routes/login";
import { Users } from "~/routes/users";
import { AuthError } from "~/utils/types";

import { CreateClient } from "./routes/clients/create";

async function authLoader({ url }: LoaderFunctionArgs) {
  const response = await fetch("/auth/me", {
    credentials: "include",
  });

  if (response.status === 401) {
    if (url.pathname === "/") {
      throw redirect("/login");
    } else {
      throw redirect(
        `/login?next=${encodeURIComponent(`${url.pathname}${url.search}${url.hash}`)}`,
      );
    }
  }

  if (!response.ok) {
    throw new AuthError("Failed to check authentication");
  }

  return response.json();
}

export default function App() {
  const router = createBrowserRouter([
    {
      element: <PublicLayout />,
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
      shouldRevalidate: () => false,
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

  return <RouterProvider router={router} />;
}
