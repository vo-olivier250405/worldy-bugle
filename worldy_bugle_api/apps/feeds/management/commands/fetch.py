from pprint import pprint

from apps.feeds.fetcher import Fetcher
from apps.feeds.models import Source
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Test the Fetcher class"

    def handle(self, *_args, **_kwargs):
        source = Source.objects.first()
        fetcher = Fetcher(source)
        feed = fetcher.fetch()

        pprint(feed)
