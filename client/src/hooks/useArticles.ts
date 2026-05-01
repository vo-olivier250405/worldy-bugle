import { useQuery } from "@tanstack/react-query";
import { articlesApi } from "@/api/articles";

export function useCountryArticles(iso: string | null) {
  return useQuery({
    queryKey: ["articles", iso],
    queryFn: () => articlesApi.list(iso!),
    enabled: iso !== null,
    staleTime: 5 * 60 * 1000,
  });
}
