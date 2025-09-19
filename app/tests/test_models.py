from .test_setup import TestModelSetup


class ModelTests(TestModelSetup):

    def test_person_str(self):
        """Test la méthode __str__ pour chaque instance de Person."""

        self.assertEqual(str(self.director), "Quentin Tarantino")
        self.assertEqual(str(self.producer), "Steven Spielberg")
        self.assertEqual(str(self.actor_1), "Leonardo DiCaprio")
        self.assertEqual(str(self.actor_2), "Brad Pitt")

    def test_movie_str(self):
        """Test la méthode __str__ pour chaque instance de Movie."""

        self.assertEqual(str(self.movie_1), "Inception")
        self.assertEqual(str(self.movie_2), "Once Upon a Time in Hollywood")

    def test_category_str(self):
        """Test la méthode __str__ pour chaque instance de Category."""

        self.assertEqual(str(self.category_1), "Science Fiction")
        self.assertEqual(str(self.category_2), "Drama")

    def test_movie_creation(self):
        """Vérifie que la création d'un film initialise correctement les champs principaux."""

        self.assertEqual(self.movie_1.title, "Inception")
        self.assertEqual(self.movie_1.duration, "2h28")

    def test_movie_relations(self):
        """Vérifie que les relations ManyToMany des films sont définies correctement."""

        self.assertIn(self.director, self.movie_1.directors.all())
        self.assertIn(self.producer, self.movie_1.producers.all())
        self.assertIn(self.actor_1, self.movie_1.actors.all())
        self.assertIn(self.category_1, self.movie_1.categories.all())
        self.assertIn(self.category_2, self.movie_1.categories.all())
        self.assertIn(self.category_2, self.movie_2.categories.all())

    def test_movies_have_categories(self):
        """Vérifie que chaque film a au moins une catégorie attribuée."""

        self.assertTrue(self.movie_1.categories.exists())
        self.assertTrue(self.movie_2.categories.exists())
