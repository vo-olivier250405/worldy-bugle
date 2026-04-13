from rest_framework.serializers import ModelSerializer

from apps.articles.models import Country


class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = ["code", "name"]


class CountryLiteSerializer(CountrySerializer):
    class Meta:
        model = Country
        fields = ["code"]
