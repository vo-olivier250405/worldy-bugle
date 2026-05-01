import { useInfiniteQuery } from "@tanstack/react-query";
import { articlesApi } from "@/api/articles";

export function useCountryArticles(iso: string | null) {
  return useInfiniteQuery({
    queryKey: ["articles", iso],
    queryFn: ({ pageParam }) => articlesApi.list(iso!, pageParam),
    initialPageParam: 1,
    getNextPageParam: (lastPage) =>
      lastPage.pager.current < lastPage.pager.total
        ? lastPage.pager.current + 1
        : undefined,
    enabled: iso !== null,
    staleTime: 5 * 60 * 1000,
  });
}
