from django.db import models


# abstract model that will provide common fields inheritable by other models
class Person(models.Model):
    name = models.CharField(max_length=200)
    imdb_id = models.CharField(max_length=20, unique=True, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Director(Person):

    class Meta:
        verbose_name_plural = "Directors"


class Producer(Person):

    class Meta:
        verbose_name_plural = "Producers"


class Actor(Person):

    class Meta:
        verbose_name_plural = "Actors"


class Movie(models.Model):
    title = models.CharField(max_length=255)
    duration = models.CharField(max_length=10)
    summary = models.TextField()
    poster_url = models.URLField()

    # Relations
    directors = models.ManyToManyField(Director, related_name="movies")
    producers = models.ManyToManyField(Producer, related_name="movies")
    actors = models.ManyToManyField(Actor, related_name="movies")

    def __str__(self):
        return self.title
