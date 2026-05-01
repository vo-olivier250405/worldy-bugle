import { requester } from "@/lib/requester";
import type { ArticleLite, PaginatedResponse } from "@/types";

export const articlesApi = {
  list: (country: string, page = 1) =>
    requester<PaginatedResponse<ArticleLite>>("articles/", {
      params: { country, page },
    }),
};
