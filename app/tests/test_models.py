from django.test import TestCase
from ..models import Movie

class MovieModelTest(TestCase):

    def setUp(self):
        self.movie = Movie.objects.create(
            title="Inception",
            duration="2h28",
            summary="A mind-bending thriller",
            poster_url="http://example.com/poster.jpg"
        )

    def test_movie_str(self):
        self.assertEqual(str(self.movie), "Inception")

    def test_movie_creation(self):
        self.assertEqual(self.movie.title, "Inception")
        self.assertEqual(self.movie.duration, "2h28")