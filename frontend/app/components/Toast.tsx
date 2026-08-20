import { Status } from "~/stores/appStore";

interface ErrorToastProps {
  message: string;
  status: Status;
  onClose: () => void;
}

export const Toast = ({ message, status, onClose }: ErrorToastProps) => {
  const style = status === Status.success ? "success" : "danger";
  return (
    <div
      className={`toast show toast-message align-items-center text-bg-${style} border-0`}
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
};
