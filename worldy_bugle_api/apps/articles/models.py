import uuid

from django.db import models


class Articles(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    resume = models.TextField()
    country = models.CharField(max_length=3)
    url = models.URLField()
    published_at = models.DateTimeField()
    source = models.ForeignKey("feeds.Source", on_delete=models.CASCADE)

    def __str__(self):
        return self.title
