export interface ArticleLite {
  id: string;
  title: string;
  countries: { code: string }[];
  url: string;
  published_at: string;
}

export interface PaginatedResponse<T> {
  next: string | null;
  previous: string | null;
  count: number;
  pager: { current: number; total: number };
  data: T[];
}
