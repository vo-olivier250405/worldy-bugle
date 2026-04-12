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

        source = Source.objects.first()
        fetcher = Fetcher(source)
        detector = DetectorUtils(source)
        entries = fetcher.get_entries()

        self.stdout.write(f"Fetched {len(entries)} entries")

        for entry in entries:
            codes_names = detector.detect_country(entry)
            published_at = detector.detect_published_date(entry)

            self.stdout.write(f"\nProcessing entry: {entry.get('title', '')}")
            self.stdout.write(f"Detected country codes: {codes_names}")

            article, created = Article.objects.get_or_create(
                title=entry.get("title", ""),
                resume=entry.get("summary", ""),
                url=entry.get("link", ""),
                published_at=published_at,
                source=source,
            )
            if not created:
                self.stdout.write(f"{article.title} skipped.")
                continue

            code_to_set = []
            for code in codes_names:
                country, _ = Country.objects.get_or_create(
                    code=code["code"], defaults={"name": code["name"]}
                )
                code_to_set.append(country)

            article.countries.set(code_to_set)
