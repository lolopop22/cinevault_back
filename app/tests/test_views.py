import logging
from unittest.mock import patch
from rest_framework import status
from django.urls import reverse_lazy

from .test_setup import TestModelSetup
from ..services import IMDbService
from ..models import Category


class TestMovieViewSet(TestModelSetup):

    def setUp(self):

        super().setUp()

        # Nettoyage des catégories pour éviter les duplicatas
        # Category.objects.all().delete()

        self.list_url = reverse_lazy("movie-list")
        self.detail_url = reverse_lazy("movie-detail", kwargs={"pk": self.movie_1.id})
        self.search_url = reverse_lazy("movie-search_movie")
        self.add_movie_url = reverse_lazy("movie-add_movie")

    def test_get_movie_list(self):
        """Vérifie la récupération de la liste des films."""

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.json()[0]["title"], self.movie_data_1.get("title"))

    def test_get_movie_detail(self):
        """Vérifie la récupération des détails d'un film spécifique."""

        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Inception")
        self.assertEqual(response.data["duration"], "2h28")
        self.assertIn("categories", response.data)
        self.assertGreater(len(response.data["categories"]), 0)

    @patch.object(IMDbService, "search_movie")
    def test_search_movies_valid(self, mock_search_movie):
        """Vérifie la recherche de films avec un titre valide."""

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
        """Vérifie qu'une recherche avec un titre vide est rejetée."""

        response = self.client.get(self.search_url, {"title": ""})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Le titre du film ne peut être vide.", response.data["title"])

    def test_search_movies_missing_title(self):
        """Vérifie que l'absence de titre déclenche une erreur de validation."""

        response = self.client.get(self.search_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Ce champ est obligatoire.", response.data["title"])

    @patch.object(IMDbService, "search_movie")
    def test_search_movies_generic_exception(self, mock_search_movie):
        """Test que l'API gère correctement les exceptions lors de la recherche."""

        mock_search_movie.side_effect = Exception("Erreur générique")
        response = self.client.get(self.search_url, {"title": "Inception"})
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("Une erreur est survenue", response.data["detail"])

    @patch.object(IMDbService, "get_movie_details")
    def test_add_movie_success(self, mock_get_movie_details):
        """Vérifie l'ajout réussi d'un nouveau film au catalogue."""

        mock_get_movie_details.return_value = {
            "imdb_id": "tt0068646",
            "title": "The Godfather",
            "duration": "2h55",
            "summary": "Crime film.",
            "poster_url": "http://example.com/godfather.jpg",
            "directors": [{"name": "Francis Ford Coppola", "imdb_id": "nm0001123"}],
            "producers": [{"name": "Albert S. Ruddy", "imdb_id": "nm0748918"}],
            "actors": [{"name": "Marlon Brando", "imdb_id": "nm0000008"}],
            "categories": [{"name": "Drama"}, {"name": "Crime"}],
        }

        # Assurez-vous que les catégories existent avant d'exécuter le test
        # for category_data in mock_get_movie_details.return_value["categories"]:
        #     Category.objects.get_or_create(name=category_data["name"])

        response = self.client.post(self.add_movie_url, {"imdb_id": "tt0068646"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch.object(IMDbService, "get_movie_details")
    def test_add_movie_duplicate(self, mock_get_movie_details):
        """Test que l'ajout d'un film déjà existant dans le catalogue échoue."""

        # Configuration du retour simulé pour get_movie_details
        mock_get_movie_details.return_value = {
            "imdb_id": self.movie_data_1["imdb_id"],
            "title": self.movie_data_1["title"],
            "duration": self.movie_data_1["duration"],
            "summary": self.movie_data_1["summary"],
            "poster_url": self.movie_data_1["poster_url"],
            "directors": [self.director_data],
            "producers": [self.producer_data],
            "actors": [self.actor_data_1],
            "categories": [self.category_data_1, self.category_data_2],
        }

        # Tenter d'ajouter le même film une deuxième fois
        response = self.client.post(
            self.add_movie_url, {"imdb_id": self.movie_data_1["imdb_id"]}
        )

        # Vérifier que le code de réponse est 400 BAD REQUEST et que le message approprié est renvoyé
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Le film existe déjà dans le catalogue.", response.data["detail"])

    def test_add_movie_with_invalid_imdb_id(self):
        """Test d'ajout avec un IMDb ID invalide."""

        response = self.client.post(self.add_movie_url, {"imdb_id": "invalid_id"})
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn(
            "Erreur lors de la récupération des détails du film",
            response.data["detail"],
        )

    def test_filter_by_category(self):
        response = self.client.get(
            reverse_lazy("movie-list"), {"categories": "Science Fiction"}
        )
        logging.debug(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for movie in response.data:
            self.assertIn("Science Fiction", movie["categories"])
