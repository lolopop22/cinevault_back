import unittest
from unittest.mock import patch, MagicMock
from imdb import IMDbError, Movie
from django.test import TestCase
from ..services import IMDbService


class TestIMDbService(TestCase):

    def setUp(self):
        self.imdb_service = IMDbService()

    @patch("imdb.IMDbBase.search_movie")
    def test_search_movies(self, mock_search_movie):
        # Simuler les résultats de recherche

        movie1 = MagicMock(movieID="tt1234567")
        movie1.__getitem__.side_effect = lambda key: {
            "title": "Inception",
            "cover url": "http://example.com/poster1.jpg",
        }.get(key)

        movie2 = MagicMock(movieID="tt7654321")
        movie2.__getitem__.side_effect = lambda key: {
            "title": "Matrix",
            "cover url": "http://example.com/poster2.jpg",
        }.get(key)

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
        mock_search_movie.side_effect = IMDbError("Simulated IMDbError")

        with self.assertRaises(IMDbError) as context:
            self.imdb_service.search_movie("InvalidTitle")

        self.assertTrue("Simulated IMDbError" in str(context.exception))

    @patch("imdb.IMDbBase.search_movie")
    def test_search_movie_generic_exception(self, mock_search_movie):
        mock_search_movie.side_effect = Exception("Erreur générique")

        with self.assertRaises(Exception) as context:
            self.imdb_service.search_movie("Inception")

        self.assertIn(
            "Erreur inconnue survenue lors de la recherche IMDb", str(context.exception)
        )
