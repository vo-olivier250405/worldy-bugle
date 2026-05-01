import { createContext, useContext, useMemo } from "react";
import type { ReactNode } from "react";
import { X, ExternalLink, Newspaper } from "lucide-react";
import { useCountryArticles } from "@/hooks/useArticles";
import type { ArticleLite } from "@/types";
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
} from "@/components/ui/sheet";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";

// ─── Context ──────────────────────────────────────────────

interface CountrySheetContextValue {
  iso: string | null;
  countryName: string | null;
  articles: ArticleLite[];
  count: number;
  isLoading: boolean;
  isError: boolean;
  onClose: () => void;
}

const CountrySheetContext = createContext<CountrySheetContextValue | null>(
  null,
);

function useCountrySheetContext() {
  const ctx = useContext(CountrySheetContext);
  if (!ctx)
    throw new Error(
      "CountrySheet sub-component must be used inside <CountrySheet>",
    );
  return ctx;
}

// ─── Root ─────────────────────────────────────────────────

interface CountrySheetProps {
  iso: string | null;
  countryName: string | null;
  onClose: () => void;
  children: ReactNode;
}

function CountrySheetRoot({
  iso,
  countryName,
  onClose,
  children,
}: CountrySheetProps) {
  const { data, isLoading, isError } = useCountryArticles(iso);

  const value = useMemo<CountrySheetContextValue>(
    () => ({
      iso,
      countryName,
      articles: data?.data ?? [],
      count: data?.count ?? 0,
      isLoading,
      isError,
      onClose,
    }),
    [iso, countryName, data, isLoading, isError, onClose],
  );

  return (
    <CountrySheetContext.Provider value={value}>
      <Sheet open={iso !== null} onOpenChange={(open) => !open && onClose()}>
        <SheetContent>{children}</SheetContent>
      </Sheet>
    </CountrySheetContext.Provider>
  );
}

// ─── Header ───────────────────────────────────────────────

function CountrySheetHeader() {
  const { countryName, count, isLoading, onClose } = useCountrySheetContext();

  return (
    <SheetHeader>
      <SheetDescription>Articles for {countryName ?? "this country"}</SheetDescription>
      <div className="flex items-start justify-between gap-3">
        <div className="flex flex-col gap-2">
          <SheetTitle>{countryName ?? "Country"}</SheetTitle>
          {!isLoading && (
            <Badge>
              {count} article{count !== 1 ? "s" : ""}
            </Badge>
          )}
          {isLoading && <Skeleton className="h-5 w-20" />}
        </div>
        <button
          onClick={onClose}
          aria-label="Close"
          className="mt-0.5 rounded p-1 text-[#9791a8] transition-colors hover:bg-[#f3f0fd] hover:text-[#1e1b2e]"
        >
          <X size={15} />
        </button>
      </div>
    </SheetHeader>
  );
}

// ─── ArticleList ──────────────────────────────────────────

function CountrySheetArticleList() {
  const { articles, isLoading, isError } = useCountrySheetContext();

  if (isLoading) {
    return (
      <div className="flex flex-col gap-2.5 p-4">
        {Array.from({ length: 6 }).map((_, i) => (
          <Skeleton key={i} className="h-[72px] w-full" />
        ))}
      </div>
    );
  }

  if (isError) {
    return (
      <div className="flex flex-col items-center justify-center gap-2 p-8 text-center">
        <p className="text-sm text-[#6b6375]">Failed to load articles.</p>
      </div>
    );
  }

  if (articles.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center gap-3 p-8 text-center">
        <Newspaper size={32} className="text-[#c4b5fd]" />
        <p className="text-sm text-[#9791a8]">
          No articles for this country yet.
        </p>
      </div>
    );
  }

  return (
    <div className="flex-1 min-h-0 overflow-hidden">
      <ScrollArea className="h-full">
        <div className="flex flex-col gap-2.5 p-4">
          {articles.map((article) => (
            <CountrySheetArticleItem key={article.id} article={article} />
          ))}
        </div>
      </ScrollArea>
    </div>
  );
}

// ─── ArticleItem ──────────────────────────────────────────

function CountrySheetArticleItem({ article }: { article: ArticleLite }) {
  return (
    <a
      href={article.url}
      target="_blank"
      rel="noreferrer"
      className="group flex flex-col gap-1.5 rounded-lg border border-[#e4dff5] bg-[#faf8ff] p-3.5 transition-all hover:border-[#c4b5fd] hover:bg-[#f3f0fd]"
    >
      <p className="line-clamp-3 text-sm font-medium leading-snug text-[#1e1b2e]">
        {article.title}
      </p>
      <div className="flex items-center justify-between gap-2">
        <div className="flex items-center gap-1.5 min-w-0">
          <time className="shrink-0 text-xs text-[#9791a8]">
            {new Date(article.published_at).toLocaleDateString("en-GB", {
              day: "numeric",
              month: "short",
              year: "numeric",
            })}
          </time>
          <span className="text-[#d8d0f0]">·</span>
          <span className="truncate text-xs text-[#9791a8]">
            {article.source.name}
          </span>
        </div>
        <ExternalLink
          size={11}
          className="shrink-0 text-[#9791a8] opacity-0 transition-opacity group-hover:opacity-100"
        />
      </div>
    </a>
  );
}

// ─── Compound export ──────────────────────────────────────

type CountrySheetComponent = typeof CountrySheetRoot & {
  Header: typeof CountrySheetHeader;
  ArticleList: typeof CountrySheetArticleList;
  ArticleItem: typeof CountrySheetArticleItem;
};

const CountrySheet = CountrySheetRoot as CountrySheetComponent;
CountrySheet.Header = CountrySheetHeader;
CountrySheet.ArticleList = CountrySheetArticleList;
CountrySheet.ArticleItem = CountrySheetArticleItem;

export { CountrySheet };
