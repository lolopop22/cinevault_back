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
    """VueSet pour gérer les opérations CRUD sur les films, avec recherche et ajout à partir de l'IMDb."""

    queryset = Movie.objects.all()
    serializer_class = MovieListSerializer
    detail_serializer_class = MovieDetailSerializer

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialisation de la VueSet pour les films avec injection de dépendance de IMDbService."""

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
        """Recherche les films sur IMDb en fonction d'un titre."""

        serializer = MovieSearchRequestSerializer(data=request.query_params)
        if serializer.is_valid():
            title = serializer.validated_data["title"]

            logging.info(f"Recherche du film {title}")
            try:
                results = self.imdb_service.search_movie(title)
                return Response(results, status=status.HTTP_200_OK)
            except Exception as e:
                logging.exception(
                    f"Une erreur est survenue lors de la recherche du film {title}: {e}"
                )
                return Response(
                    {"detail": "Une erreur est survenue"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            logging.warning("Les paramètres de recherche ne sont pas valides.")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path="add", url_name="add_movie")
    def add_movie(self, request):
        """Ajoute un film au catalogue via un identifiant IMDb."""

        serializer = MovieAddRequestSerializer(data=request.data)
        if serializer.is_valid():
            imdb_id = serializer.validated_data["imdb_id"]

            logging.info(
                f"Tentative d'ajout du film avec l'ID IMDb : {imdb_id} au catalogue"
            )
            try:
                if Movie.objects.filter(imdb_id=imdb_id).exists():
                    logging.warning(f"Le film avec l'ID IMDb {imdb_id} existe déjà.")
                    return Response(
                        {"detail": "Le film existe déjà dans le catalogue."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                movie_details = self.imdb_service.get_movie_details(imdb_id)
                logging.debug(f"Détails du film récupérés: {movie_details}")
                detail_serializer = self.detail_serializer_class(data=movie_details)
                if detail_serializer.is_valid():
                    detail_serializer.save()
                    logging.info(f"Film avec l'ID {imdb_id} ajouté au catalogue.")
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                logging.error(
                    f"Erreurs de validation lors de l'ajout du film : {detail_serializer.errors}"
                )
                return Response(
                    detail_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except Exception as e:
                logging.exception(f"Erreur lors de l'ajout du film avec l'ID {imdb_id}")
                return Response(
                    {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            logging.warning(f"Erreur d'entrée: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
