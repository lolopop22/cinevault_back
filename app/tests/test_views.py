from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse_lazy
from .test_setup import TestModelSetup


class TestMovieViewSet(TestModelSetup):

    def setUp(self):

        super().setUp()

        self.url = reverse_lazy("movie-list")
        self.detail_url = reverse_lazy("movie-detail", kwargs={"pk": self.movie_1.id})

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
