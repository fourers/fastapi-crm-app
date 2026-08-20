import { useRouteError } from "react-router-dom";

import { AuthError } from "~/utils/types";

export const ErrorScreen = () => {
  const error = useRouteError() as Error;
  const title =
    error instanceof AuthError ? "Authentication Error" : "Unexpected Error";

  const handleRetry = () => {
    window.location.reload();
  };

  return (
    <div
      className="container d-flex align-items-center justify-content-center"
      style={{ minHeight: "100vh" }}
    >
      <div className="text-center">
        <h1 className="display-4 mb-4">{title}</h1>
        <p className="lead text-muted mb-4">{error.message}</p>
        <div className="d-flex gap-2 justify-content-center">
          <button className="btn btn-dark w-100" onClick={handleRetry}>
            Reload
          </button>
          <a href="/login" className="btn btn-dark w-100">
            Login
          </a>
        </div>
      </div>
    </div>
  );
};
