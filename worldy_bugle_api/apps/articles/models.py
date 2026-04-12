import uuid

from django.db import models


class Country(models.Model):
    code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.code


class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    resume = models.TextField()
    countries = models.ManyToManyField(Country, related_name="articles")
    url = models.URLField()
    published_at = models.DateTimeField()
    source = models.ForeignKey("feeds.Source", on_delete=models.CASCADE)

    def __str__(self):
        return self.title
