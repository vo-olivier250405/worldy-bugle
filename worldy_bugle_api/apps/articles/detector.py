import time
from datetime import datetime, timezone
from typing import Any, TypedDict

import geograpy
import pycountry
import spacy
from feedparser import FeedParserDict

from apps.feeds.models import Source


class CountryCodeNameType(TypedDict):
    name: str
    code: str


class DetectorUtils:
    def __init__(self, source: Source):
        self.source = source
        spacy.prefer_gpu()
        self.nlp = spacy.load("en_core_web_trf")

    def _resolve_country_code(self, name: str) -> str | None:
        try:
            country = pycountry.countries.search_fuzzy(name)
            return country[0].alpha_3
        except LookupError:
            return None

    def _get_codes_from_link(self, link: str) -> list[CountryCodeNameType] | list[None]:
        places = geograpy.get_geoPlace_context(url=link)
        codes = []
        for country in places.countries:
            if code := self._resolve_country_code(country):
                codes.append({"name": country, "code": code})
        return codes

    def _get_code_from_GPE(self, text: str) -> CountryCodeNameType | None:
        doc = self.nlp(text)
        for ent in doc.ents:
            if ent.label_ != "GPE":
                continue
            if code := self._resolve_country_code(ent.text):
                return {"name": ent.text, "code": code}
        return None

    def detect_country(
        self, feed_entry: Any | FeedParserDict
    ) -> list[CountryCodeNameType]:
        text = f"{feed_entry.get('title', '')} {feed_entry.get('summary', '')}"
        link = feed_entry.get("link", None)

        if code := self._get_code_from_GPE(text):
            return [code]

        if link and (code := self._get_codes_from_link(link)):
            return code

        return [{"name": "Unknown", "code": "UNK"}]

    def detect_published_date(self, feed_entry: Any | FeedParserDict):
        parsed = feed_entry.get("published_parsed")
        if parsed is None:
            return None
        return datetime.fromtimestamp(time.mktime(parsed), tz=timezone.utc)
