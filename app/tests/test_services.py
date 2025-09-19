import unittest
from unittest.mock import patch, MagicMock
from imdb import IMDbError

# from imdbinfo.models import MovieDetail, Person
from django.test import TestCase
from ..services import IMDbService


class TestIMDbService(TestCase):
    """Tests unitaires pour le service IMDb."""

    def setUp(self):
        """Configuration des tests, initialise le service IMDb."""

        self.imdb_service = IMDbService()

    @patch("imdb.IMDbBase.search_movie")
    def test_search_movies(self, mock_search_movie):
        """Test la recherche de films via l'API IMDb avec des résultats simulés."""

        movie1 = MagicMock(movieID="tt1234567")
        movie1.get.side_effect = lambda key, default="": {
            "title": "Inception",
            "cover url": "http://example.com/poster1.jpg",
        }.get(key, default)

        movie2 = MagicMock(movieID="tt7654321")
        movie2.get.side_effect = lambda key, default="": {
            "title": "Matrix",
            "cover url": "http://example.com/poster2.jpg",
        }.get(key, default)

        mock_search_movie.return_value = [movie1, movie2]

        results = self.imdb_service.search_movie("Inception", limit=2)
        self.assertEqual(len(results), 2)

        expected = [
            {
                "imdb_id": "tt1234567",
                "title": "Inception",
                "poster_url": "http://example.com/poster1.jpg",
            },
            {
                "imdb_id": "tt7654321",
                "title": "Matrix",
                "poster_url": "http://example.com/poster2.jpg",
            },
        ]

        self.assertEqual(results, expected)

    @patch("imdb.IMDbBase.search_movie")
    def test_search_movies_imdb_error(self, mock_search_movie):
        """Test que la méthode lève une erreur IMDbError correctement."""

        mock_search_movie.side_effect = IMDbError("Simulated IMDbError")

        with self.assertRaises(IMDbError) as context:
            self.imdb_service.search_movie("InvalidTitle")

        self.assertTrue("Simulated IMDbError" in str(context.exception))

    @patch("imdb.IMDbBase.search_movie")
    def test_search_movie_generic_exception(self, mock_search_movie):
        """Test de la levée d'une exception générique et gestion."""

        mock_search_movie.side_effect = Exception("Erreur générique")

        with self.assertRaises(Exception) as context:
            self.imdb_service.search_movie("Inception")

        self.assertIn(
            "Erreur survenue lors de l'interaction avec IMDb", str(context.exception)
        )

    @patch(
        "app.services.get_movie"
    )  # le `patch()` doit viser le module où la fonction à mocker est utilisée, pas là où elle est définie
    def test_get_movie_details_success(self, mock_get_movie):
        """Test la récupération réussie des détails d'un film."""

        # on utilise un vrai MovieDetail => le code est ainsi plus robuste
        # movie = MovieDetail(
        #     id="0111161",
        #     imdb_id="0111161",
        #     imdbId="tt0111161",
        #     title="The Shawshank Redemption",
        #     duration=142,
        #     plot="Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
        #     cover_url="http://example.com/shawshank.jpg",
        #     directors=[Person(name="Frank Darabont", imdbId="ttt000001")],
        #     producers=[Person(name="Niki Marvin", imdbId="ttt000002")],
        #     stars=[
        #         Person(name="Tim Robbins", imdbId="ttt000003"),
        #         Person(name="Morgan Freeman", imdbId="ttt000004"),
        #     ],
        # )
        # Procéder ainsi rend le code fragile , moins robuste...
        movie_mock = MagicMock()
        movie_mock.title = "The Shawshank Redemption"
        movie_mock.duration = 142
        movie_mock.plot = "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency."
        movie_mock.cover_url = "http://example.com/shawshank.jpg"
        movie_mock.genres = ["Drama", "Crime"]

        director = MagicMock()
        director.name = "Frank Darabont"
        director.imdbId = "ttt000001"

        producer = MagicMock()
        producer.name = "Niki Marvin"
        producer.imdbId = "ttt000002"

        actor = MagicMock()
        actor.name = "Tim Robbins"
        actor.imdbId = "ttt000003"

        movie_mock.directors = [director]
        movie_mock.producers = [producer]
        movie_mock.stars = [actor]

        mock_get_movie.return_value = movie_mock

        details = self.imdb_service.get_movie_details("0111161")
        self.assertEqual(details["imdb_id"], "0111161")
        self.assertEqual(details["title"], "The Shawshank Redemption")
        self.assertEqual(details["duration"], "2h22")
        self.assertEqual(
            details["summary"],
            "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
        )
        self.assertEqual(details["poster_url"], "http://example.com/shawshank.jpg")
        self.assertIn(
            {"name": "Frank Darabont", "imdb_id": "ttt000001"}, details["directors"]
        )
        self.assertIn(
            {"name": "Tim Robbins", "imdb_id": "ttt000003"}, details["actors"]
        )
        self.assertIn({"name": "Drama"}, details["categories"])
        self.assertIn({"name": "Crime"}, details["categories"])

    @patch("imdbinfo.services.get_movie")
    def test_get_movie_details_general_exception(self, mock_get_movie):
        """Vérifie que les exceptions générales sont levées correctement."""

        mock_get_movie.side_effect = Exception("Simulated Exception")

        with self.assertRaises(Exception) as context:
            self.imdb_service.get_movie_details("invalid_id")

        self.assertTrue(
            "Erreur lors de la récupération des détails" in str(context.exception)
        )
