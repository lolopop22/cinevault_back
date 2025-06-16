from rest_framework import serializers
from .models import Movie, Director, Producer, Actor


class PersonBaseSerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True)
    imdb_id = serializers.CharField(read_only=True)

    class Meta:
        fields = "__all__"


class DirectorSerializer(PersonBaseSerializer, serializers.ModelSerializer):

    class Meta:
        model = Director
        fields = PersonBaseSerializer.Meta.fields


class ProducerSerializer(PersonBaseSerializer, serializers.ModelSerializer):

    class Meta:
        model = Producer
        fields = PersonBaseSerializer.Meta.fields


class ActorSerializer(PersonBaseSerializer, serializers.ModelSerializer):

    class Meta:
        model = Actor
        fields = PersonBaseSerializer.Meta.fields


class MovieListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ("id", "title", "poster_url")


class MovieDetailSerializer(serializers.ModelSerializer):

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
