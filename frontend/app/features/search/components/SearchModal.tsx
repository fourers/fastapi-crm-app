import { keepPreviousData, useQuery } from "@tanstack/react-query";
import { useEffect, useState } from "react";
import { useForm, useWatch } from "react-hook-form";

import type { SearchResult } from "~/features/search/api/types";

interface SearchModalProps {
  show: boolean;
  onHide: () => void;
  searchFunc: (q: string) => Promise<SearchResult[]>;
}

function useDebounce<T>(value: T, delay: number) {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timeout = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => clearTimeout(timeout);
  }, [value, delay]);

  return debouncedValue;
}

export const SearchModal = ({ show, onHide, searchFunc }: SearchModalProps) => {
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
  const { data, isFetching } = useQuery({
    queryKey: ["search", trimmedQuery],
    queryFn: () => searchFunc(trimmedQuery),
    enabled: hasQuery,
    placeholderData: keepPreviousData,
    staleTime: 30_000,
  });

  return (
    <div
      className={`modal fade ${show ? "show d-block" : ""}`}
      tabIndex={-1}
      role="dialog"
    >
      <div className="modal-dialog modal-dialog-centered modal-lg">
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

            <div className="border-top">
              {hasQuery && isFetching && <div className="p-3 text-muted">Searching...</div>}
              {hasQuery && !isFetching &&
                (data ?? []).map((result) => (
                  <a
                    key={result.id}
                    className="list-group-item list-group-item-action py-3"
                  >
                    <strong>{result.name}</strong>
                  </a>
                ))}
              {hasQuery && !isFetching && (data ?? []).length === 0 && (
                <div className="p-3 text-muted">No results found.</div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
