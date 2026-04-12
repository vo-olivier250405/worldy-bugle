from pprint import pprint

from apps.articles.detector import DetectorUtils
from apps.articles.models import Article, Country
from apps.feeds.fetcher import Fetcher
from apps.feeds.models import Source
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Test the Fetcher class"

    def handle(self, *_args, **_kwargs):
        # Article.objects.all().delete()
        # Country.objects.all().delete()

        for source in Source.objects.all():
            try:
                errors_url = []

                fetcher = Fetcher(source)
                detector = DetectorUtils(source)
                entries = fetcher.get_new_entries()

                for entry in entries:
                    codes_names = detector.detect_country(entry)
                    published_at = detector.detect_published_date(entry)

                    # self.stdout.write(f"\nProcessing entry: {entry.get('title', '')}")
                    # self.stdout.write(f"Detected country codes: {codes_names}")

                    article = Article.objects.create(
                        title=entry.get("title", ""),
                        resume=entry.get("summary", ""),
                        url=entry.get("link", ""),
                        published_at=published_at,
                        source=source,
                    )

                    code_to_set = []
                    for code in codes_names:
                        country, _ = Country.objects.get_or_create(
                            code=code["code"], defaults={"name": code["name"]}
                        )
                        code_to_set.append(country)

                    article.countries.set(code_to_set)
            except Exception as e:
                errors_url.append({"url": entry.get("link", ""), "error": e.__str__()})

            if errors_url:
                self.stdout.write("\nErrors occurred for the following URLs:")
                pprint(errors_url)

            self.stdout.write(f"Finished processing source: {source.name}")
