import django_filters

from apps.articles.models import Article


class ArticleFilter(django_filters.FilterSet):
    country = django_filters.CharFilter(
        field_name="countries__code", lookup_expr="iexact"
    )

    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    resume = django_filters.CharFilter(field_name="resume", lookup_expr="icontains")
    url = django_filters.CharFilter(field_name="url", lookup_expr="iexact")
    source = django_filters.CharFilter(field_name="source__name", lookup_expr="iexact")
    published_at = django_filters.DateFromToRangeFilter(field_name="published_at")

    class Meta:
        model = Article
        fields = ["country", "title", "resume", "url", "source", "published_at"]
