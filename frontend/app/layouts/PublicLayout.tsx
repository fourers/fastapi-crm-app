import { Outlet } from "react-router-dom";

export function PublicLayout() {
  return (
    <>
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
        <div className="container align-items-center justify-content-center">
          <a className="navbar-brand" href="/">
            FastAPI CRM
          </a>
        </div>
      </nav>

      <main className="container py-4">
        <Outlet />
      </main>
    </>
  );
}
