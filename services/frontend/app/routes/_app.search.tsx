import { useState } from "react";
import {
  ProcessingApi,
  type SearchResultsResponse,
  type ProcessingResponse,
} from "clients/orchestrator";
import { useInfiniteQuery } from "@tanstack/react-query";
import { config } from "~/configs";
import { useDebounce } from "use-debounce";
import { SearchHero } from "../components/search/SearchHero";
import { SearchInput } from "../components/search/SearchInput";
import { SearchResults } from "../components/search/SearchResults";

const RESULTS_PER_PAGE = 2;

export default function SearchPage() {
  const [searchQuery, setSearchQuery] = useState("");
  const api = new ProcessingApi(config);
  const [debouncedSearchQuery] = useDebounce(searchQuery, 400);
  const [fetched, setFetched] = useState(false);

  const { isLoading, isError, data, error, fetchNextPage, hasNextPage, isFetchingNextPage } =
    useInfiniteQuery<SearchResultsResponse>({
      queryKey: ["search", debouncedSearchQuery],
      initialPageParam: 1,
      queryFn: async ({ pageParam }) => {
        const response = await api.searchResultsByQueryProcessSearchGet(
          debouncedSearchQuery,
          RESULTS_PER_PAGE,
          pageParam as number
        );
        setFetched(true);
        return response.data;
      },
      getNextPageParam: (
        lastPage: SearchResultsResponse,
        allPages: SearchResultsResponse[]
      ): number | undefined => {
        const currentCount = allPages.reduce((total, page) => total + page.items.length, 0);
        const totalCount = lastPage.total;
        return currentCount < totalCount ? allPages.length + 1 : undefined;
      },
      enabled: true,
    });

  // Flatten all pages into a single results array
  const allResults: ProcessingResponse[] =
    data?.pages?.reduce((acc, page) => [...acc, ...page.items], [] as ProcessingResponse[]) || [];

  const totalResults = data?.pages?.[0]?.total || 0;

  return (
    <div className="container mx-auto px-4 py-12 lg:py-16">
      <div className="max-w-2xl mx-auto space-y-8">
        <SearchHero />
        <SearchInput value={searchQuery} onChange={setSearchQuery} />
        <SearchResults
          results={allResults}
          isLoading={isLoading}
          isError={isError}
          error={error as Error | null}
          hasSearched={searchQuery.trim().length > 0}
          totalResults={totalResults}
          hasNextPage={hasNextPage ?? false}
          isFetchingNextPage={isFetchingNextPage}
          fetchNextPage={fetchNextPage}
        />
      </div>
    </div>
  );
}
