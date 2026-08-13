import "bootstrap/dist/css/bootstrap.min.css";
import "~/app.css";

import { redirect } from "react-router";
import { createBrowserRouter, type LoaderFunctionArgs, RouterProvider } from "react-router-dom";

import { LoadingScreen } from "~/components/LoadingScreen";
import { AppLayout } from "~/layouts/AppLayout";
import { PublicLayout } from "~/layouts/PublicLayout";
import { NotFound } from "~/routes/404";
import { Clients } from "~/routes/Clients";
import { Home } from "~/routes/Home";
import { Login } from "~/routes/Login";

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
    throw new Error("Failed to check authentication");
  }

  return response.json();
}

export default function App() {
  const router = createBrowserRouter([
    {
      element: <PublicLayout />,
      HydrateFallback: LoadingScreen,
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
      HydrateFallback: LoadingScreen,
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
          path: "*",
          element: <NotFound />,
        },
      ],
    },
    {
      path: "/loading",
      element: <LoadingScreen />,
    },
  ]);

  return <RouterProvider router={router} />;
}
