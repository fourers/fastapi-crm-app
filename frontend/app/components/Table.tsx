import { Link } from "react-router-dom";

import { LoadingSpinner } from "~/components/LoadingSpinner";
import type { JSONValue } from "~/lib/types";

interface TableProps {
  rows: JSONValue[];
  loading: boolean;
  loadingMessage: string;
  emptyMessage: string;
  editButtonLink?: (data: JSONValue) => string;
}

export const Table = ({
  rows,
  loading,
  loadingMessage,
  emptyMessage,
  editButtonLink,
}: TableProps) => {
  const columns = rows.length > 0 ? Object.keys(rows[0]) : [];

  return (
    <>
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
                  {editButtonLink && <th scope="col"></th>}
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
                    {editButtonLink && (
                      <td className="text-nowrap" style={{ width: "1%" }}>
                        <Link to={editButtonLink(row)}>Edit</Link>
                      </td>
                    )}
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
    </>
  );
};
