import type { ReactNode } from "react";

import type { SearchResult } from "~/features/search/api/types";

interface ModalResultsProps {
  data: SearchResult[];
  appendComponent?: (data: SearchResult) => ReactNode;
}

export const ModalResults = ({ data, appendComponent }: ModalResultsProps) => (
  <div className="p-3 table-responsive">
    <table className="table table-hover table-borderless align-middle mb-0">
      <tbody>
        {data.map((result) => (
          <tr key={result.id}>
            <td>
              <div className="d-block text-decoration-none">{result.name}</div>
            </td>
            {appendComponent && (
              <td className="text-nowrap" style={{ width: "1%" }}>
                {appendComponent(result)}
              </td>
            )}
          </tr>
        ))}
      </tbody>
    </table>
  </div>
);
