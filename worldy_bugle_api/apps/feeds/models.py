from django.db import models


class Source(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
    country_code = models.CharField(max_length=3, blank=True, null=True)

    def __str__(self):
        return self.name
