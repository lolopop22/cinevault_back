from django.db import models


class Person(models.Model):
    """Modèle abstrait pour une personne associée à un film, comme un directeur, un producteur ou un acteur."""

    name = models.CharField(max_length=200)
    imdb_id = models.CharField(max_length=20, unique=True, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Director(Person):
    """Modèle pour un réalisateur de film."""

    class Meta:
        verbose_name_plural = "Directors"


class Producer(Person):
    """Modèle pour un producteur de film."""

    class Meta:
        verbose_name_plural = "Producers"


class Actor(Person):
    """Modèle pour un acteur de film."""

    class Meta:
        verbose_name_plural = "Actors"


class Category(models.Model):
    """Modèle pour définir une catégorie de film."""

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Movie(models.Model):
    """Modèle pour un film, comprenant des relations avec réalisateurs, producteurs, acteurs et catégories."""

    imdb_id = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=255)
    duration = models.CharField(max_length=10, default="Non indiqué")
    summary = models.TextField(default="Non indiqué")
    poster_url = models.URLField(blank=True)

    # Relations
    directors = models.ManyToManyField(Director, related_name="movies", blank=True)
    producers = models.ManyToManyField(Producer, related_name="movies", blank=True)
    actors = models.ManyToManyField(Actor, related_name="movies", blank=True)
    categories = models.ManyToManyField(Category, related_name="movies", blank=True)

    def __str__(self):
        return self.title
