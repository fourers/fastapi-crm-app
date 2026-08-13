import { ErrorToast } from "~/components/ErrorToast";
import { useErrorStore } from "~/stores/errorStore";

export function GlobalErrorToast() {
  const errors = useErrorStore((state) => state.errors);

  if (errors.length === 0) {
    return null;
  }

  return (
    <div
      className="toast-container position-fixed top-0 start-50 translate-middle-x p-5"
      style={{ zIndex: 1080 }}
    >
      {errors.map((error) => {
        const prefix = error.status ? `${error.status}: ` : "";
        return (
          <ErrorToast
            error={`${prefix}${error.message}`}
            onClose={() => useErrorStore.getState().removeError(error.id)}
          />
        );
      })}
    </div>
  );
}
