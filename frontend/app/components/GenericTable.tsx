import { type ReactNode } from "react";

import { LoadingSpinner } from "~/components/LoadingSpinner";
import type { JSONValue } from "~/lib/types";

interface GenericTableProps {
  rows: JSONValue[];
  loading: boolean;
  loadingMessage: string;
  emptyMessage: string;
  appendComponent?: (data: JSONValue) => ReactNode;
}

export const GenericTable = ({
  rows,
  loading,
  loadingMessage,
  emptyMessage,
  appendComponent,
}: GenericTableProps) => {
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
                  {appendComponent && <th scope="col"></th>}
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
                    {appendComponent && (
                      <td className="text-nowrap" style={{ width: "1%" }}>
                        {appendComponent(row)}
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
