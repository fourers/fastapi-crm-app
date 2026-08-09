import { Outlet } from "react-router-dom";

export function AppLayout() {
  return (
    <>
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
        <div className="container">
          <a className="navbar-brand" href="/">FastAPI CRM</a>
          <div className="collapse navbar-collapse" id="navbarNav">
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
        </div>
      </nav>

      <main className="container py-4">
        <Outlet />
      </main>
    </>
  );
}
