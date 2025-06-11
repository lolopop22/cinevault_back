from .test_setup import TestModelSetup


class ModelTests(TestModelSetup):

    def test_person_str(self):
        self.assertEqual(str(self.director), "Quentin Tarantino")
        self.assertEqual(str(self.producer), "Steven Spielberg")
        self.assertEqual(str(self.actor_1), "Leonardo DiCaprio")
        self.assertEqual(str(self.actor_2), "Brad Pitt")

    def test_movie_str(self):
        self.assertEqual(str(self.movie_1), "Inception")
        self.assertEqual(str(self.movie_2), "Once Upon a Time in Hollywood")

    def test_movie_creation(self):
        self.assertEqual(self.movie_1.title, "Inception")
        self.assertEqual(self.movie_1.duration, "2h28")

    def test_movie_relations(self):
        self.assertIn(self.director, self.movie_1.directors.all())
        self.assertIn(self.producer, self.movie_1.producers.all())
        self.assertIn(self.actor_1, self.movie_1.actors.all())
