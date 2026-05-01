from rest_framework import serializers

from apps.articles.models import Article

from .country_serializer import CountryLiteSerializer, CountrySerializer
from .source_serializer import SourceLiteSerializer, SourceSerializer


class ArticleSerializer(serializers.ModelSerializer):
    countries = CountrySerializer(many=True)
    source = SourceSerializer()

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "resume",
            "countries",
            "url",
            "published_at",
            "source",
        ]


class ArticleLiteSerializer(ArticleSerializer):
    countries = CountryLiteSerializer(many=True)
    source = SourceLiteSerializer()

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "countries",
            "url",
            "published_at",
            "source",
        ]
