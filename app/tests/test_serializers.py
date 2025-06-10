from django.test import TestCase
from ..models import Movie
from ..serializers import MovieSerializer


class MovieSerializerTest(TestCase):

    def setUp(self):
        self.movie = Movie.objects.create(
            title="Inception",
            duration="2h28",
            summary="A mind-bending thriller",
            poster_url="http://example.com/poster.jpg"
        )
        self.serializer = MovieSerializer(instance=self.movie)

    def test_serialization(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'title', 'duration', 'summary', 'poster_url'})
        self.assertEqual(data['title'], "Inception")