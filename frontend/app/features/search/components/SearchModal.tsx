import { keepPreviousData, useQuery } from "@tanstack/react-query";
import { type ReactNode, useCallback, useEffect, useState } from "react";
import { useForm, useWatch } from "react-hook-form";

import type { SearchResult } from "~/features/search/api/types";
import { ModalResults } from "~/features/search/components/ModalResults";
import { queryClient } from "~/lib/queryClient";

interface SearchModalProps {
  show: boolean;
  disabled: boolean;
  onHide: () => void;
  searchFunc: (q: string) => Promise<SearchResult[]>;
  appendComponent?: (data: SearchResult) => ReactNode;
  resetKey?: number;
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

export const SearchModal = ({
  show,
  disabled,
  onHide,
  searchFunc,
  appendComponent,
  resetKey,
}: SearchModalProps) => {
  const { control, register, reset } = useForm({
    defaultValues: { query: "" },
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
  });

  const resetSearch = useCallback(() => {
    reset({ query: "" });
    queryClient.removeQueries({ queryKey: ["search"] });
  }, [reset]);

  const onClose = () => {
    resetSearch();
    onHide();
  };

  useEffect(() => {
    resetSearch();
  }, [resetKey, resetSearch]);

  return (
    <>
      {show && <div className="modal-backdrop fade show" aria-hidden="true" />}
      <div
        className={`modal fade ${show ? "show d-block" : ""}`}
        tabIndex={-1}
        role="dialog"
      >
        <div className="modal-dialog">
          <div className="modal-content">
            <div className="modal-body p-0">
              <div className="input-group input-group-lg">
                <span className="input-group-text border-0 bg-transparent">
                  🔍
                </span>

                <input
                  {...register("query")}
                  type="search"
                  autoComplete="off"
                  className="form-control border-0 shadow-none"
                  placeholder="Search..."
                  autoFocus
                  disabled={disabled}
                />

                <button
                  type="button"
                  className="btn btn-link text-secondary"
                  onClick={onClose}
                  disabled={disabled}
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
