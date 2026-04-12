import logging

from celery import shared_task


@shared_task
def fetch_new_articles():
    from apps.articles.detector import DetectorUtils
    from apps.articles.models import Article, Country

    from .fetcher import Fetcher
    from .models import Source

    all_sources = Source.objects.all()

    for source in all_sources:
        try:
            errors_url = []

            fetcher = Fetcher(source)
            detector = DetectorUtils(source)
            entries = fetcher.get_new_entries()

            for entry in entries:
                codes_names = detector.detect_country(entry)
                published_at = detector.detect_published_date(entry)

                article = Article.objects.create(
                    title=entry.get("title", ""),
                    resume=entry.get("summary", ""),
                    url=entry.get("link", ""),
                    published_at=published_at,
                    source=source,
                )

                codes_to_set = []
                for code in codes_names:
                    country, _ = Country.objects.get_or_create(
                        code=code["code"], defaults={"name": code["name"]}
                    )
                    codes_to_set.append(country)

                article.countries.set(codes_to_set)

        except Exception as e:
            errors_url.append({"url": entry.get("link", ""), "error": e.__str__()})

        if errors_url:
            logging.error("\nErrors occurred for the following URLs: ")
            for error in errors_url:
                logging.error(f"URL: {error['url']} - Error: {error['error']}")
        logging.info(f"Finished processing source: {source.name}")
