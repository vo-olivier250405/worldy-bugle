from rest_framework.serializers import ModelSerializer

from apps.feeds.models import Source


class SourceSerializer(ModelSerializer):
    class Meta:
        model = Source
        fields = ["name", "url"]


class SourceLiteSerializer(ModelSerializer):
    class Meta:
        model = Source
        fields = ["name"]
