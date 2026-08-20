import { Toast } from "~/components/Toast";
import { useAppStore } from "~/stores/appStore";

export const GlobalToast = () => {
  const { messages } = useAppStore();

  if (messages.length === 0) {
    return null;
  }

  return (
    <div
      className="toast-container position-fixed top-0 start-50 translate-middle-x p-5"
      style={{ zIndex: 1080 }}
    >
      {messages.map((message) => {
        return (
          <Toast
            key={message.id}
            message={message.message}
            status={message.status}
            onClose={() => useAppStore.getState().removeMessage(message.id)}
          />
        );
      })}
    </div>
  );
};
