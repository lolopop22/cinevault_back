import logging

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from typing import Any

from .models import Movie
from .serializers import (
    MovieListSerializer,
    MovieDetailSerializer,
    MovieSearchRequestSerializer,
    MovieAddRequestSerializer,
)

from .container import injector
from .services import IMDbService


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieListSerializer
    detail_serializer_class = MovieDetailSerializer

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        logging.info("Initialisation de la vue gérant les films")
        super().__init__(*args, **kwargs)
        self.imdb_service: IMDbService = injector.get(
            IMDbService
        )  # Pour l'injection des dépendances

    def get_serializer_class(self):
        if self.action == "retrieve":
            return self.detail_serializer_class
        return super().get_serializer_class()

    @action(detail=False, methods=["get"], url_path="search", url_name="search_movie")
    def search_movies(self, request):
        serializer = MovieSearchRequestSerializer(data=request.query_params)
        if serializer.is_valid():
            title = serializer.validated_data["title"]

            logging.info(f"Recherche du film {title}")
            try:
                results = self.imdb_service.search_movie(title)
                return Response(results, status=status.HTTP_200_OK)
            except Exception as e:
                logging.exception(f"Une erreur est survenue: {e}")
                return Response(
                    {"detail": "Une erreur est survenue"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path="add", url_name="add_movie")
    def add_movie(self, request):
        """Ajoute un film au catalogue via un identifiant IMDb."""

        serializer = MovieAddRequestSerializer(data=request.data)
        if serializer.is_valid():
            imdb_id = serializer.validated_data["imdb_id"]

            try:
                logging.info(f"Ajout du film d'id IMDb '{imdb_id}' au catalogue.")
                if Movie.objects.filter(imdb_id=imdb_id).exists():
                    return Response(
                        {"detail": "Le film existe déjà dans le catalogue."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                movie_details = self.imdb_service.get_movie_details(imdb_id)
                logging.debug(f"movie_details: {movie_details}")
                detail_serializer = self.detail_serializer_class(data=movie_details)
                if detail_serializer.is_valid():
                    detail_serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(
                    detail_serializer.errors,
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            except Exception as e:
                logging.exception("Erreur lors de l'ajout du film.")
                return Response(
                    {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
