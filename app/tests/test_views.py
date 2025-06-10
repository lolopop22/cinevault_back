from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse_lazy
from ..models import Movie


class TestMovies(APITestCase):


    def setUp(self):
        self.url = reverse_lazy('movie-list')
        self.movie_data_1 = {
            "title": "Inception",
            "duration": "2h28",
            "summary": "A mind-bending thriller",
            "poster_url": "http://example.com/poster.jpg"
        }
        self.movie_1 = Movie.objects.create(**self.movie_data_1)

        self.movie_data_2 = {
            "title": "The Dark Knight",
            "duration": "2h32",
            "summary": "When the menace known as The Joker emerges from his mysterious past, he wreaks havoc and chaos on the people of Gotham.",
            "poster_url": "http://example.com/darkknight.jpg"
        }
        self.movie_2 = Movie.objects.create(**self.movie_data_2)

    def test_get_movie_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.json()[0]["title"], self.movie_data_1.get("title"))