import type { RouteObject } from "react-router-dom";

import { AppLayout } from "~/layouts/AppLayout";
import { ErrorLayout } from "~/layouts/ErrorLayout";
import { PublicLayout } from "~/layouts/PublicLayout";
import { Home } from "~/pages";
import { NotFound } from "~/pages/404";
import { Clients } from "~/pages/clients";
import { CreateClient } from "~/pages/clients/create";
import { UpdateClient } from "~/pages/clients/update";
import { Login } from "~/pages/login";
import { Users } from "~/pages/users";
import { authLoader, loginLoader } from "~/router/loader";

export const routes: RouteObject[] = [
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
    errorElement: <ErrorLayout />,
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
];
