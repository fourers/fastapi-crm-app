import { Link, Outlet, useNavigation } from "react-router-dom";

import { LoadingSpinner } from "~/components/LoadingSpinner";

export const PublicLayout = () => {
  const navigation = useNavigation();

  return (
    <>
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
        <div className="container align-items-center justify-content-center">
          <Link className="navbar-brand" to="/">
            FastAPI CRM
          </Link>
        </div>
      </nav>

      {navigation.state === "loading" && <LoadingSpinner />}

      <main className="container py-4">
        <Outlet />
      </main>
    </>
  );
};
