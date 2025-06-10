from rest_framework import viewsets
from .models import Movie
from .serializers import MovieListSerializer, MovieDetailSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieListSerializer
    detail_serializer_class = MovieDetailSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return self.detail_serializer_class
        return super().get_serializer_class()