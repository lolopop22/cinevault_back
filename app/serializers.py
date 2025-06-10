from rest_framework import serializers
from .models import Movie

class MovieListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Movie
        fields = ('id', 'title', 'poster_url')


class MovieDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('id', 'title', 'duration', 'summary', 'poster_url')
