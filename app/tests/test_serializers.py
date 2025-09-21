from .test_setup import TestModelSetup
from ..serializers import (
    MovieListSerializer,
    MovieDetailSerializer,
    MovieAddRequestSerializer,
)


class SerializerTest(TestModelSetup):

    def test_movie_list_serializer(self):
        """Vérifie que le sérialiseur MovieList contient les champs requis et sérialise correctement."""

        data = MovieListSerializer(instance=self.movie_1).data
        self.assertEqual(set(data.keys()), {"id", "title", "poster_url", "categories"})
        self.assertEqual(data["title"], self.movie_data_1["title"])
        self.assertEqual(
            data["poster_url"],
            self.movie_data_1["poster_url"],
        )

    def test_movie_detail_serializer(self):
        """Vérifie que le sérialiseur des détails de film intègre correctement toutes les relations et champs."""

        data = MovieDetailSerializer(instance=self.movie_1).data
        self.movie_data_1.update(
            {
                "directors": [self.director_data],
                "producers": [self.producer_data],
                "actors": [self.actor_data_1],
                "categories": [self.category_data_1, self.category_data_2],
            }
        )

        self.assertEqual(
            set(data.keys()),
            {
                "id",
                "imdb_id",
                "title",
                "duration",
                "summary",
                "poster_url",
                "directors",
                "producers",
                "actors",
                "categories",
            },
        )
        self.assertEqual(data["title"], self.movie_data_1["title"])
        self.assertEqual(data["duration"], self.movie_data_1["duration"])
        self.assertEqual(data["summary"], self.movie_data_1["summary"])
        self.assertEqual(data["poster_url"], self.movie_data_1["poster_url"])
        self.assertEqual(
            data["directors"][0]["name"], self.movie_data_1["directors"][0]["name"]
        )
        self.assertEqual(
            data["producers"][0]["name"], self.movie_data_1["producers"][0]["name"]
        )
        self.assertEqual(
            data["actors"][0]["name"], self.movie_data_1["actors"][0]["name"]
        )
        self.assertEqual(
            data["categories"][0]["name"], self.movie_data_1["categories"][0]["name"]
        )
        self.assertEqual(
            data["categories"][1]["name"], self.movie_data_1["categories"][1]["name"]
        )

    def test_add_movie_serializer_valid_data(self):
        """Vérifie que les données valides passent la validation."""

        serializer = MovieAddRequestSerializer(data=self.valid_imdb_id_data)
        self.assertTrue(serializer.is_valid())

    def test_add_movie_serializer_invalid_blank_imdb_id(self):
        """Vérifie que l'identifiant IMDb vide échoue à la validation."""

        serializer = MovieAddRequestSerializer(data=self.invalid_imdb_id_data_blank)
        self.assertFalse(serializer.is_valid())
        self.assertIn("imdb_id", serializer.errors)
        self.assertEqual(
            serializer.errors["imdb_id"][0],
            "L'identifiant IMDb de ce film ne peut être vide",
        )

    def test_add_movie_serializer_id_imdb_trop_long(self):
        """Vérifie qu'un identifiant IMDb trop long échoue à la validation."""

        serializer = MovieAddRequestSerializer(data=self.invalid_imdb_id_data_long)
        self.assertFalse(serializer.is_valid())
        self.assertIn("imdb_id", serializer.errors)
        self.assertEqual(
            serializer.errors["imdb_id"][0],
            "Assurez-vous que ce champ ne comporte pas plus de 10 caractères.",
        )
