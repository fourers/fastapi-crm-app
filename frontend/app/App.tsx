import "bootstrap/dist/css/bootstrap.min.css";
import "./app.css";

import { redirect } from "react-router";
import { createBrowserRouter, RouterProvider } from "react-router-dom";

import { AppLayout } from "./layouts/AppLayout";
import { PublicLayout } from "./layouts/PublicLayout";
import { NotFound } from "./routes/404";
import { Home } from "./routes/home";
import { Login } from "./routes/login";

async function authLoader() {
  const response = await fetch("/auth/me", {
    credentials: "include",
  });

  if (response.status === 401) {
    throw redirect("/login");
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
      children: [
        {
          path: "/",
          element: <Home />,
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
