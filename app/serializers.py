from rest_framework import serializers
from .models import Movie, Director, Producer, Actor


class PersonBaseSerializer(serializers.ModelSerializer):
    """Sérializer de base gérant les données liées à des personnes"""

    class Meta:
        fields = ("name", "imdb_id")


class DirectorSerializer(PersonBaseSerializer):
    """Serializer for Director model."""

    class Meta(PersonBaseSerializer.Meta):
        model = Director


class ProducerSerializer(PersonBaseSerializer):
    """Serializer for Producer model."""

    class Meta(PersonBaseSerializer.Meta):
        model = Producer


class ActorSerializer(PersonBaseSerializer):
    """Serializer for Actor model."""

    class Meta(PersonBaseSerializer.Meta):
        model = Actor


class MovieListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ("id", "title", "poster_url")


class MovieDetailSerializer(serializers.ModelSerializer):
    """Serializer détaillé pour le modèle Movie."""

    directors = DirectorSerializer(many=True)
    producers = ProducerSerializer(many=True)
    actors = ActorSerializer(many=True)

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
        )

    def create(self, validated_data):
        directors_data = validated_data.pop("directors")
        producers_data = validated_data.pop("producers")
        actors_data = validated_data.pop("actors")

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

        return movie


class MovieSearchRequestSerializer(serializers.Serializer):
    title = serializers.CharField(
        max_length=255,
        required=True,
        error_messages={"blank": "Le titre du film ne peut être vide."},
    )


class MovieAddRequestSerializer(serializers.Serializer):
    imdb_id = serializers.CharField(
        max_length=10,
        required=True,
        error_messages={"blank": "L'identifiant IMDb de ce film ne peut être vide"},
    )
