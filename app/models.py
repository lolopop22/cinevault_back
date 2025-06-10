from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=255)
    duration = models.CharField(max_length=10)
    summary = models.TextField()
    poster_url = models.URLField()

    def __str__(self):
        return self.title
