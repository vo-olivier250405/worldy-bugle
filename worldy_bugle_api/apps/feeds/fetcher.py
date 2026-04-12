import feedparser as fp

from apps.articles.models import Article
from apps.feeds.models import Source


class Fetcher:
    def __init__(self, source: Source):
        self.source = source

    def _fetch(self):
        return fp.parse(self.source.url)

    def get_entries(self):
        return self._fetch().entries

    def get_new_entries(self):
        entries = self.get_entries()
        if not entries:
            return []
        entries_urls = [e.get("link", None) for e in entries]

        existing_articles = Article.objects.filter(url__in=entries_urls)
        existing_urls = set(existing_articles.values_list("url", flat=True))
        new_entries = [e for e in entries if e.get("link", None) not in existing_urls]
        print(f"\nTotal entries fetched: {len(entries)}")
        print(f"Existing articles in DB with same URLs: {existing_articles.count()}")
        print(f"New entries to be added: {len(new_entries)}")
        return new_entries
