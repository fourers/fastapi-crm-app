export function Home() {
  return (
    <>
      <h1 className="display-5 pt-3 pb-3" style={{ textAlign: "center" }}>
        You are logged in
      </h1>

      <div className="d-flex justify-content-center p-3">
        <div style={{ width: "100%", maxWidth: "200px" }}>
          <a href="/clients" className="btn btn-secondary btn-lg w-100 mb-3">
            View Clients
          </a>
          <a href="/users" className="btn btn-secondary btn-lg w-100">
            View Users
          </a>
        </div>
      </div>
    </>
  );
}
