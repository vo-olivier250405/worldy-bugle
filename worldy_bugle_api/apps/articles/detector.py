from typing import Any

import pycountry
import spacy
from feedparser import FeedParserDict

from apps.feeds.models import Source


class DetectorUtils:
    def __init__(self, source: Source):
        self.source = source
        if self.source.country_code is None:
            spacy.prefer_gpu()
            self.nlp = spacy.load("en_core_web_sm")

    def _resolve_country_code(self, name: str) -> str | None:
        try:
            country = pycountry.countries.search_fuzzy(name)
            return country[0].alpha_2
        except LookupError:
            return None

    def detect_country(self, feed_entry: Any | FeedParserDict) -> str:

        text = f"{feed_entry.get('title', '')} {feed_entry.get('summary', '')}"
        doc = self.nlp(text)

        for ent in doc.ents:
            if ent.label_ != "GPE":
                continue

            code = self._resolve_country_code(ent.text)
            if code:
                return code

        if self.source.country_code is not None:
            return self.source.country_code

        return "Unknown"
