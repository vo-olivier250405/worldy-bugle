from rest_framework import serializers

from apps.articles.models import Article


class ArticleSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "countries",
            "url",
            "published_at",
        ]
