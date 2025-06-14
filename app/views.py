from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from typing import Any

from .models import Movie
from .serializers import (
    MovieListSerializer,
    MovieDetailSerializer,
    MovieSearchSerializer,
)

from .container import injector
from .services import IMDbService


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieListSerializer
    detail_serializer_class = MovieDetailSerializer

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.imdb_service: IMDbService = injector.get(
            IMDbService
        )  # Pour l'injection des dépendances

    def get_serializer_class(self):
        if self.action == "retrieve":
            return self.detail_serializer_class
        return super().get_serializer_class()

    @action(detail=False, methods=["get"], url_path="search", url_name="search")
    def search_movies(self, request):
        serializer = MovieSearchSerializer(data=request.query_params)
        if serializer.is_valid():
            title = serializer.validated_data["title"]

            try:
                results = self.imdb_service.search_movie(title)
                return Response(results, status=status.HTTP_200_OK)
            except Exception as e:
                print(str(e))
                return Response(
                    {"detail": "Une erreur est survenue"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
