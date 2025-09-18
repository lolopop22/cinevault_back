from rest_framework.test import APITestCase
from ..models import Movie, Director, Producer, Actor


class TestModelSetup(APITestCase):

    def setUp(self):

        self.director_data = {"name": "Quentin Tarantino", "imdb_id": "nm0000233"}
        self.producer_data = {"name": "Steven Spielberg", "imdb_id": "nm0000229"}
        self.actor_data_1 = {"name": "Leonardo DiCaprio", "imdb_id": "nm0000138"}
        self.actor_data_2 = {"name": "Brad Pitt", "imdb_id": "nm0000123"}

        self.movie_data_1 = {
            "imdb_id": "tt1234567",
            "title": "Inception",
            "duration": "2h28",
            "summary": "A mind-bending thriller",
            "poster_url": "http://example.com/poster.jpg",
        }

        self.movie_data_2 = {
            "imdb_id": "tt7654321",
            "title": "Once Upon a Time in Hollywood",
            "duration": "2h39m",
            "summary": "A movie about Hollywood in the 60s.",
            "poster_url": "http://example.com/poster.jpg",
        }

        # Créez des instances de modèles pour les tests
        self.director = Director.objects.create(**self.director_data)
        self.producer = Producer.objects.create(**self.producer_data)
        self.actor_1 = Actor.objects.create(**self.actor_data_1)
        self.actor_2 = Actor.objects.create(**self.actor_data_2)

        self.movie_1 = Movie.objects.create(**self.movie_data_1)
        self.movie_2 = Movie.objects.create(**self.movie_data_2)

        # Ajouter des relations ManyToMany
        self.movie_1.directors.add(self.director)
        self.movie_1.producers.add(self.producer)
        self.movie_1.actors.add(self.actor_1)

        self.movie_2.directors.add(self.director)
        self.movie_2.producers.add(self.producer)
        self.movie_2.actors.add(self.actor_2)

        self.valid_imdb_id_data = {"imdb_id": "tt0111161"}
        self.invalid_imdb_id_data_blank = {"imdb_id": ""}
        self.invalid_imdb_id_data_long = {
            "imdb_id": "tt0111161234"  # Exceeds maximum length
        }
