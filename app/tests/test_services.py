import unittest
from unittest.mock import patch, MagicMock
from imdb import IMDbError
from django.test import TestCase
from ..services import IMDbService


class TestIMDbService(TestCase):

    def setUp(self):
        self.imdb_service = IMDbService()

    @patch("imdb.IMDbBase.search_movie")
    def test_search_movies(self, mock_search_movie):
        # Simuler les résultats de recherche

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

    @patch("imdb.IMDbBase.get_movie")
    def test_get_movie_details_success(self, mock_get_movie):
        # Mock a successful response from IMDb API
        mock_get_movie.return_value = MagicMock(
            get=lambda key, default="": {
                "title": "The Shawshank Redemption",
                "runtime": [142],
                "plot": [
                    "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency."
                ],
                "cover url": "http://example.com/shawshank.jpg",
                "genres": ["Drama"],
                "directors": [{"name": "Frank Darabont"}],
                "producers": [{"name": "Niki Marvin"}],
                "cast": [{"name": "Tim Robbins"}, {"name": "Morgan Freeman"}],
            }.get(key, default)
        )

        # Test successful retrieval of movie details
        details = self.imdb_service.get_movie_details("0111161")
        self.assertEqual(details["imdb_id"], "0111161")
        self.assertEqual(details["title"], "The Shawshank Redemption")
        self.assertEqual(details["duration"], "2h22")
        self.assertEqual(
            details["summary"],
            "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
        )
        self.assertEqual(details["poster_url"], "http://example.com/shawshank.jpg")
        self.assertIn("Drama", details["categories"])
        self.assertIn("Frank Darabont", details["directors"])
        self.assertIn("Tim Robbins", details["actors"])

    @patch("imdb.IMDbBase.get_movie")
    def test_get_movie_details_imdb_error(self, mock_get_movie):
        # Simulate an IMDbError exception
        mock_get_movie.side_effect = IMDbError("Simulated IMDbError")

        with self.assertRaises(IMDbError) as context:
            self.imdb_service.get_movie_details("invalid_id")

        self.assertTrue("Simulated IMDbError" in str(context.exception))

    @patch("imdb.IMDbBase.get_movie")
    def test_get_movie_details_general_exception(self, mock_get_movie):
        # Simulate a general exception
        mock_get_movie.side_effect = Exception("Simulated Exception")

        with self.assertRaises(Exception) as context:
            self.imdb_service.get_movie_details("invalid_id")

        self.assertTrue(
            "Erreur lors de la récupération des détails" in str(context.exception)
        )
