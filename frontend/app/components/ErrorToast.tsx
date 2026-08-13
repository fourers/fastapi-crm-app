import { type AppError } from "~/stores/errorStore";

interface ErrorToastProps {
  error: AppError;
  onClose: () => void;
}

export function ErrorToast({ error, onClose }: ErrorToastProps) {
  const prefix = error.status ? `${error.status}: ` : "";
  const message = `${prefix}${error.message}`;
  return (
    <div
      className="toast show align-items-center text-bg-danger border-0"
      role="alert"
      aria-live="assertive"
      aria-atomic="true"
    >
      <div className="d-flex">
        <div className="toast-body">{message}</div>
        <button
          type="button"
          className="btn-close btn-close-white me-2 m-auto"
          aria-label="Close"
          onClick={onClose}
        />
      </div>
    </div>
  );
}
