export function Login() {
  return (
    <div className="d-flex align-items-center justify-content-center">
      <div className="card shadow-sm m-4" style={{ width: "100%", maxWidth: "400px" }}>
        <div className="card-body p-5 text-center">
          <h1 className="h3 mb-3">Welcome</h1>

          <p className="text-muted mb-4">Sign in to continue</p>

          <a href="/auth/login" className="btn btn-dark btn-lg w-100">
            Login
          </a>
        </div>
      </div>
    </div>
  );
}
