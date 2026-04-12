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
        entries_urls = [e.get("url", "") for e in entries]
        if not entries_urls:
            return []

        existing_articles = Article.objects.filter(url__in=entries_urls)
        existing_urls = set(existing_articles.values_list("url", flat=True))
        return [e for e in entries if e.get("url", "") not in existing_urls]
