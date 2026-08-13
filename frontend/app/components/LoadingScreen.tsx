import { LoadingSpinner } from "~/components/LoadingSpinner";

export function LoadingScreen() {
  return (
    <main className="min-vh-100 d-flex align-items-center justify-content-center">
      <LoadingSpinner />
    </main>
  );
}
