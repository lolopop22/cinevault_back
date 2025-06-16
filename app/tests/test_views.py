from unittest.mock import patch
from rest_framework import status
from django.urls import reverse_lazy

from .test_setup import TestModelSetup
from ..services import IMDbService


class TestMovieViewSet(TestModelSetup):

    def setUp(self):

        super().setUp()

        self.url = reverse_lazy("movie-list")
        self.detail_url = reverse_lazy("movie-detail", kwargs={"pk": self.movie_1.id})
        self.search_url = reverse_lazy("movie-search_movie")

    def test_get_movie_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.json()[0]["title"], self.movie_data_1.get("title"))

    def test_get_movie_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Inception")
        self.assertEqual(response.data["duration"], "2h28")

    @patch.object(IMDbService, "search_movie")
    def test_search_movies_valid(self, mock_search_movie):
        mock_search_movie.return_value = [
            {
                "imdb_id": "tt0111161",
                "title": "The Shawshank Redemption",
                "poster_url": "http://example.com/shawshank.jpg",
            },
            {
                "imdb_id": "tt0068646",
                "title": "The Godfather",
                "poster_url": "http://example.com/godfather.jpg",
            },
        ]
        response = self.client.get(self.search_url, {"title": "Inception"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("imdb_id", response.data[0])
        self.assertIn("title", response.data[0])
        self.assertIn("poster_url", response.data[0])

    @patch.object(IMDbService, "search_movie")
    def test_search_movies_blank_title(self, mock_search_movie):
        response = self.client.get(self.search_url, {"title": ""})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Le titre du film ne peut être vide.", response.data["title"])

    def test_search_movies_missing_title(self):
        response = self.client.get(self.search_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This field is required.", response.data["title"])

    @patch.object(IMDbService, "search_movie")
    def test_search_movies_generic_exception(self, mock_search_movie):
        mock_search_movie.side_effect = Exception("Erreur générique")
        response = self.client.get(self.search_url, {"title": "Inception"})
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("Une erreur est survenue", response.data["detail"])
