import { useEffect, useState } from "react";

interface ErrorToastProps {
  error: string | null;
}

export function ErrorToast({ error }: ErrorToastProps) {
  const [showToast, setShowToast] = useState(false);
  useEffect(() => {
    console.log(error);
    if (error) {
      setShowToast(true);
    }
  }, [error]);

  return (
    <div
      className="toast-container position-fixed top-0 start-50 translate-middle-x p-5"
      style={{ zIndex: 1080 }}
    >
      {showToast && error && (
        <div
          className="toast show align-items-center text-bg-danger border-0"
          role="alert"
          aria-live="assertive"
          aria-atomic="true"
        >
          <div className="d-flex">
            <div className="toast-body">{error}</div>
            <button
              type="button"
              className="btn-close btn-close-white me-2 m-auto"
              aria-label="Close"
              onClick={() => setShowToast(false)}
            />
          </div>
        </div>
      )}
    </div>
  );
}
