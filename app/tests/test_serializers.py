from .test_setup import TestModelSetup
from ..serializers import MovieListSerializer, MovieDetailSerializer


class SerializerTest(TestModelSetup):

    def test_movie_list_serializer(self):
        data = MovieListSerializer(instance=self.movie_1).data
        self.assertEqual(set(data.keys()), {"id", "title", "poster_url"})
        self.assertEqual(data["title"], self.movie_data_1["title"])
        self.assertEqual(
            data["poster_url"],
            self.movie_data_1["poster_url"],
        )

    def test_movie_detail_serializer(self):
        data = MovieDetailSerializer(instance=self.movie_1).data
        self.movie_data_1.update(
            {
                "directors": [self.director_data],
                "producers": [self.producer_data],
                "actors": [self.actor_data_1],
            }
        )

        self.assertEqual(
            set(data.keys()),
            {
                "id",
                "title",
                "duration",
                "summary",
                "poster_url",
                "directors",
                "producers",
                "actors",
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
