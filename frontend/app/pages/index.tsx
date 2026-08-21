import { Link } from "react-router-dom";

export const Home = () => {
  return (
    <>
      <h1 className="display-5 pt-3 pb-3" style={{ textAlign: "center" }}>
        You are logged in
      </h1>

      <div className="d-flex justify-content-center p-3">
        <div
          className="list-group"
          style={{ width: "100%", maxWidth: "250px" }}
        >
          <Link
            to="/clients"
            className="list-group-item list-group-item-action text-center"
          >
            Clients
          </Link>
          <Link
            to="/users"
            className="list-group-item list-group-item-action text-center"
          >
            Users
          </Link>
        </div>
      </div>
    </>
  );
};
