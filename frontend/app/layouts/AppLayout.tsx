import { Outlet, useNavigation } from "react-router-dom";

import { GlobalToast } from "~/components/GlobalToast";
import { LoadingSpinner } from "~/components/LoadingSpinner";

export const AppLayout = () => {
  const navigation = useNavigation();

  return (
    <>
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
        <div className="container">
          <a className="navbar-brand" href="/">
            FastAPI CRM
          </a>
          <ul className="navbar-nav ms-auto">
            <li className="nav-item">
              <form method="post" action="/auth/logout">
                <button type="submit" className="nav-link btn btn-link">
                  Logout
                </button>
              </form>
            </li>
          </ul>
        </div>
      </nav>

      {navigation.state === "loading" && <LoadingSpinner />}

      <GlobalToast />

      <main className="container py-4">
        <Outlet />
      </main>
    </>
  );
};
