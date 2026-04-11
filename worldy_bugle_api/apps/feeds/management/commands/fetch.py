from pprint import pprint

from apps.articles.detector import DetectorUtils
from apps.feeds.fetcher import Fetcher
from apps.feeds.models import Source
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Test the Fetcher class"

    def handle(self, *_args, **_kwargs):
        source = Source.objects.first()
        fetcher = Fetcher(source)
        detector = DetectorUtils(source)
        entries = fetcher.get_entries()
        for entry in entries:
            country = detector.detect_country(entry)
            print("\n")
            pprint(country)
            pprint(entry.get("title", "No title"))
