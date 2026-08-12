import { LoadingSpinner } from "~/components/LoadingSpinner";
import { type Client } from "~/stores/clientStore";

interface TableProps {
  clients: Client[];
  loading: boolean;
}

export function ClientTable({ clients, loading }: TableProps) {
  return (
    <div className="card shadow-sm">
      <div className="card-header">
        <h5 className="mb-0">Clients</h5>
      </div>

      <div className="card-body">
        {loading ? (
          <div id="loading" className="text-center py-4">
            <LoadingSpinner />
            <p className="mb-4 text-muted">Loading clients...</p>
          </div>
        ) : (
          <div id="table-container" className="table-responsive">
            <table className="table table-hover align-middle mb-0">
              <thead id="table-head">
                {clients.length > 0 ? (
                  <tr>
                    <th scope="col">#</th>
                    <th scope="col">First Name</th>
                    <th scope="col">Last Name</th>
                    <th scope="col">Email</th>
                    <th scope="col">Owner Id</th>
                  </tr>
                ) : null}
              </thead>
              <tbody id="table-body">
                {clients.length === 0 ? (
                  <tr>
                    <td colSpan={100} className="text-center text-muted py-4">
                      No clients found.
                    </td>
                  </tr>
                ) : null}
                {clients.map((client) => (
                  <tr>
                    <td>{client.id}</td>
                    <td>{client.first_name}</td>
                    <td>{client.last_name}</td>
                    <td>{client.email}</td>
                    <td>{client.owner_id}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
