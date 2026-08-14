import { LoadingSpinner } from "~/components/LoadingSpinner";
import type { JSONValue } from "~/utils/types";

interface TableProps {
  rows: JSONValue[];
  loading: boolean;
  title: string;
  loadingMessage: string;
  emptyMessage: string;
}

export function Table({ rows, loading, title, loadingMessage, emptyMessage }: TableProps) {
  const columns = rows.length > 0 ? Object.keys(rows[0]) : [];

  return (
    <div className="card shadow-sm">
      <div className="card-header">
        <h5 className="mb-0">{title}</h5>
      </div>

      <div className="card-body">
        {loading ? (
          <div id="loading" className="text-center py-4">
            <LoadingSpinner />
            <p className="mb-4 text-muted">{loadingMessage}</p>
          </div>
        ) : (
          <div id="table-container" className="table-responsive">
            <table className="table table-hover align-middle mb-0">
              <thead id="table-head">
                {rows.length > 0 ? (
                  <tr>
                    {columns.map((column) => (
                      <th scope="col">{column}</th>
                    ))}
                  </tr>
                ) : null}
              </thead>
              <tbody id="table-body">
                {rows.length > 0 ? (
                  rows.map((row) => (
                    <tr>
                      {columns.map((column) => (
                        <td>{row[column]}</td>
                      ))}
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={100} className="text-center text-muted py-4">
                      {emptyMessage}
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
