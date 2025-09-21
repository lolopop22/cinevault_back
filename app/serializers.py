import logging

from rest_framework import serializers
from .models import Movie, Director, Producer, Actor, Category


class PersonBaseSerializer(serializers.ModelSerializer):
    """Sérializer de base gérant les données liées à des personnes"""

    class Meta:
        fields = ("name", "imdb_id")


class DirectorSerializer(PersonBaseSerializer):
    """Serializer pour le modèle Director."""

    class Meta(PersonBaseSerializer.Meta):
        model = Director


class ProducerSerializer(PersonBaseSerializer):
    """Serializer pour le modèle Producer."""

    class Meta(PersonBaseSerializer.Meta):
        model = Producer


class ActorSerializer(PersonBaseSerializer):
    """Serializer fpour le modèle Acteur."""

    class Meta(PersonBaseSerializer.Meta):
        model = Actor


class CategorySerializer(serializers.ModelSerializer):
    """Sérialiseur pour le modèle Category."""

    class Meta:
        model = Category
        fields = ("id", "name")

    def to_internal_value(self, data):
        """
        Personnalise la méthode to_internal_value pour gérer l'existence de catégories.

        Cette méthode est redéfinie pour vérifier l'existence des catégories avant leur création,
        afin de prévenir les erreurs dues à la contrainte d'unicité sur le champ 'name'.
        Lors de la validation, le sérialiseur essaierait de créer une nouvelle catégorie pour chaque
        entrée, même si celle-ci existe déjà, ce qui provoque une erreur de duplicata.
        Nous vérifions donc l'existence de la catégorie à ce stade et récupérons l'instance existante
        si elle est déjà en base, sinon on passe pour permettre la création.

        Args:
            data (str|dict): Données passées au sérialiseur pour le champ 'name' de la catégorie.

        Returns:
            dict: Instance de catégorie (sous forme de dict) ou données sous forme de dict.

        Raises:
            serializers.ValidationError: Si le champ 'name' est vide.
        """
        if isinstance(data, dict):
            name = data.get("name", None)
        else:
            name = data

        if not name:
            raise serializers.ValidationError(
                "Le nom de la catégorie doit être fourni."
            )

        try:
            category = Category.objects.get(name=name)
            return {
                "name": category.name,
                "id": category.id,
            }  # Retourne les données formatées
        except Category.DoesNotExist:
            return {"name": name}  # Permet la création d'une nouvelle catégorie


class MovieListSerializer(serializers.ModelSerializer):
    """Sérialiseur pour lister les films avec informations minimales, incluant les catégories."""

    categories = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )

    class Meta:
        model = Movie
        fields = ("id", "title", "poster_url", "categories")


class MovieDetailSerializer(serializers.ModelSerializer):
    """Sérialiseur détaillé pour le modèle Movie, intégrant les relations
    avec réalisateurs, producteurs, acteurs et catégories."""

    directors = DirectorSerializer(many=True)
    producers = ProducerSerializer(many=True)
    actors = ActorSerializer(many=True)
    categories = CategorySerializer(many=True)

    class Meta:
        model = Movie
        fields = (
            "id",
            "imdb_id",
            "title",
            "duration",
            "summary",
            "poster_url",
            "directors",
            "producers",
            "actors",
            "categories",
        )

    def create(self, validated_data):
        """Crée une instance de film en effectuant les relations ManyToMany pour les sous-modèles."""

        directors_data = validated_data.pop("directors")
        producers_data = validated_data.pop("producers")
        actors_data = validated_data.pop("actors")
        categories_data = validated_data.pop("categories")

        movie = Movie.objects.create(**validated_data)

        for director_data in directors_data:
            director, _ = Director.objects.get_or_create(**director_data)
            movie.directors.add(director)

        for producer_data in producers_data:
            producer, _ = Producer.objects.get_or_create(**producer_data)
            movie.producers.add(producer)

        for actor_data in actors_data:
            actor, _ = Actor.objects.get_or_create(**actor_data)
            movie.actors.add(actor)

        for category_data in categories_data:
            category, _ = Category.objects.get_or_create(name=category_data["name"])
            movie.categories.add(category)

        return movie


class MovieSearchRequestSerializer(serializers.Serializer):
    """Sérialiseur pour gérer les requêtes de recherche de films par titre."""

    title = serializers.CharField(
        max_length=255,
        required=True,
        error_messages={"blank": "Le titre du film ne peut être vide."},
    )


class MovieAddRequestSerializer(serializers.Serializer):
    """Sérialiseur pour requêtes d'ajout de film par identifiant IMDb."""

    imdb_id = serializers.CharField(
        max_length=10,
        required=True,
        error_messages={
            "blank": "L'identifiant IMDb de ce film ne peut être vide",
            "max_length": "Assurez-vous que ce champ ne comporte pas plus de 10 caractères.",
        },
    )
