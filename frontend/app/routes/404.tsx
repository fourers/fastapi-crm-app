import { useLocation } from "react-router-dom";

export function NotFound() {
  const location = useLocation();

  return (
    <div style={{ textAlign: "center" }}>
      <h1 className="display-1">404</h1>
      <h1 className="display-5">Page not found: {location.pathname}</h1>
    </div>
  );
}
