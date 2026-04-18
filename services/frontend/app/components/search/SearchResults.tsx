import type { ProcessingResponse } from "clients/orchestrator";
import type { FetchNextPageOptions } from "@tanstack/react-query";
import { Button } from "../ui/button";
import { SearchResultItem } from "./SearchResultItem";

interface SearchResultsProps {
  results: ProcessingResponse[];
  isLoading: boolean;
  isError: boolean;
  error: Error | null;
  hasSearched: boolean;
  totalResults: number;
  hasNextPage: boolean;
  isFetchingNextPage: boolean;
  fetchNextPage: (options?: FetchNextPageOptions | undefined) => Promise<any>;
}

export function SearchResults({
  results,
  isLoading,
  isError,
  error,
  hasSearched,
  totalResults,
  hasNextPage,
  isFetchingNextPage,
  fetchNextPage,
}: SearchResultsProps) {
  if (isLoading) {
    return (
      <div className="space-y-4 pt-4">
        {[...Array(3)].map((_, i) => (
          <div key={i} className="h-24 bg-slate-100 dark:bg-slate-800 rounded-lg animate-pulse" />
        ))}
      </div>
    );
  }

  if (isError) {
    return (
      <div className="p-4 bg-red-50 dark:bg-red-950 border border-red-200 dark:border-red-900 rounded-lg">
        <p className="text-red-600 dark:text-red-400">
          Error: {error instanceof Error ? error.message : "Failed to search"}
        </p>
      </div>
    );
  }

  if (results.length > 0) {
    return (
      <div className="space-y-4 pt-4">
        <p className="text-sm text-slate-600 dark:text-slate-400">
          Found {results.length} of {totalResults} result{totalResults !== 1 ? "s" : ""}
        </p>
        <div className="space-y-3">
          {results.map((result) => (
            <SearchResultItem key={result.id} result={result} />
          ))}
        </div>

        {hasNextPage && (
          <div className="pt-6 flex justify-center">
            <Button
              onClick={() => fetchNextPage()}
              disabled={isFetchingNextPage}
              variant="outline"
              size="lg"
              className="bg-gradient-to-br from-white/70 via-blue-100/60 to-purple-100/60 dark:from-white/10 dark:via-white/5 dark:to-white/10 backdrop-blur-md border border-white/40 dark:border-white/30 hover:border-white/60 dark:hover:border-white/50 text-slate-900 dark:text-white hover:text-slate-900 dark:hover:text-white hover:shadow-md transition-all"
            >
              {isFetchingNextPage ? "Loading more..." : "Load More"}
            </Button>
          </div>
        )}
      </div>
    );
  }

  if (hasSearched) {
    return (
      <div className="text-center pt-8">
        <p className="text-slate-600 dark:text-slate-400">No results found for your search.</p>
      </div>
    );
  }

  return (
    <div className="text-center pt-8">
      <p className="text-slate-600 dark:text-slate-400">
        Start typing to search for karaoke tracks...
      </p>
    </div>
  );
}
