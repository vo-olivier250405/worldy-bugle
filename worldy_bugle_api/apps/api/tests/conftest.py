import pytest
from django.utils import timezone

from apps.articles.models import Article
from apps.feeds.models import Source


@pytest.fixture
def source(db):
    return Source.objects.create(name="BBC", url="https://bbc.com")


@pytest.fixture
def article(db, source):
    return Article.objects.create(
        title="Test",
        url="https://bbc.com/1",
        source=source,
        published_at=timezone.now(),
    )


@pytest.fixture
def paginated_response_attributes():
    return {"next", "previous", "count", "pager", "data"}
