import { keepPreviousData, useQuery } from "@tanstack/react-query";
import { type ReactNode, useEffect, useState } from "react";
import { useForm, useWatch } from "react-hook-form";

import type { SearchResult } from "~/features/search/api/types";

interface SearchModalProps {
  show: boolean;
  onHide: () => void;
  searchFunc: (q: string) => Promise<SearchResult[]>;
  appendComponent?: (data: SearchResult) => ReactNode;
}

const useDebounce = <T,>(value: T, delay: number) => {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timeout = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => clearTimeout(timeout);
  }, [value, delay]);

  return debouncedValue;
};

const ModalResults = ({
  data,
  appendComponent,
}: {
  data: SearchResult[];
  appendComponent?: (data: SearchResult) => ReactNode;
}) => (
  <div className="p-3 table-responsive">
    <table className="table table-hover table-borderless align-middle mb-0">
      <tbody>
        {data.map((result) => (
          <tr key={result.id}>
            <td>
              <div className="d-block text-decoration-none">{result.name}</div>
            </td>
            {appendComponent && <td>{appendComponent(result)}</td>}
          </tr>
        ))}
      </tbody>
    </table>
  </div>
);

export const SearchModal = ({
  show,
  onHide,
  searchFunc,
  appendComponent,
}: SearchModalProps) => {
  const { control, register } = useForm({
    defaultValues: {
      query: "",
    },
  });
  const query = useWatch({
    control,
    name: "query",
  });
  const debouncedQuery = useDebounce(query, 300);
  const trimmedQuery = debouncedQuery.trim();
  const hasQuery = trimmedQuery.length > 0;
  const { data, isLoading } = useQuery({
    queryKey: ["search", trimmedQuery],
    queryFn: () => searchFunc(trimmedQuery),
    enabled: hasQuery,
    placeholderData: keepPreviousData,
    staleTime: 30_000,
  });

  return (
    <>
      {show && <div className="modal-backdrop fade show" aria-hidden="true" />}
      <div
        className={`modal fade ${show ? "show d-block" : ""}`}
        tabIndex={-1}
        role="dialog"
      >
        <div className="modal-dialog modal-lg">
          <div className="modal-content">
            <div className="modal-body p-0">
              <div className="input-group input-group-lg">
                <span className="input-group-text border-0 bg-transparent">
                  🔍
                </span>

                <input
                  {...register("query")}
                  type="search"
                  className="form-control border-0 shadow-none"
                  placeholder="Search..."
                  autoFocus
                />

                <button
                  type="button"
                  className="btn btn-link text-secondary"
                  onClick={onHide}
                >
                  <kbd>Esc</kbd>
                </button>
              </div>

              {hasQuery && (
                <div className="border-top">
                  {hasQuery && isLoading ? (
                    <div className="p-4 text-muted">Searching...</div>
                  ) : (data ?? []).length !== 0 ? (
                    <ModalResults
                      data={data!}
                      appendComponent={appendComponent}
                    />
                  ) : (
                    <div className="p-4 text-muted">No results found.</div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </>
  );
};
