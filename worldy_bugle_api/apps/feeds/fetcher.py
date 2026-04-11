from abc import ABC

import feedparser as fp
from apps.feeds.models import Source


class Fetcher(ABC):
    def __init__(self, source: Source):
        self.source = source

    def fetch(self):
        return fp.parse(self.source.url)
