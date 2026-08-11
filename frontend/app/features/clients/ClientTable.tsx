import { LoadingSpinner } from "~/components/LoadingSpinner";
import { type Client } from "~/stores/clientStore";

interface TableProps {
  clients: Client[];
  loading: boolean;
}

export function Table({ clients, loading }: TableProps) {
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
                <tr>
                  {Object.keys(clients[0] ?? []).map((col) => {
                    return <th scope="col">{col}</th>;
                  })}
                </tr>
              </thead>
              <tbody id="table-body">
                {clients.map((client) => {
                  return (
                    <tr>
                      {Object.values(client).map((value) => {
                        return <td>{value}</td>;
                      })}
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
