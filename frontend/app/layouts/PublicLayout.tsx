import { Outlet, useNavigation } from "react-router-dom";

import { LoadingSpinner } from "../components/LoadingSpinner";

export function PublicLayout() {
  const navigation = useNavigation();

  return (
    <>
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
        <div className="container align-items-center justify-content-center">
          <a className="navbar-brand" href="/">
            FastAPI CRM
          </a>
        </div>
      </nav>

      {navigation.state === "loading" && <LoadingSpinner />}

      <main className="container py-4">
        <Outlet />
      </main>
    </>
  );
}
