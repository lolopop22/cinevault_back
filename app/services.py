import os
import logging
from injector import singleton
from imdb import Cinemagoer, IMDbError
from imdbinfo.services import get_movie
from typing import List, Dict


@singleton
class IMDbService:
    """Service pour interagir avec IMDb et récupérer des données de film."""

    def __init__(self):
        """Initialise le service IMDb en configurant l'API Cinemagoer."""

        self.ia = Cinemagoer()

    def search_movie(
        self, title: str, limit: int = int(os.getenv("SEARCH_FILM_LIMIT"))
    ) -> List[Dict]:
        """
        Recherche des films sur IMDb par titre.

        Args:
            title (str): Le titre du film à rechercher.
            limit (int): Nombre maximum de films à retourner.

        Returns:
            List[Dict]: Liste de dictionnaires contenant les détails des films trouvés.

        Raises:
            IMDbError: Si une erreur se produit avec l'API IMDb.
            RuntimeError: Pour d'autres erreurs lors de la recherche.
        """
        logging.info(f"Recherche du film {title}")

        try:
            results = self.ia.search_movie(title)
            movies_data = [
                {
                    "imdb_id": movie.movieID,
                    "title": movie.get("title", ""),
                    "poster_url": movie.get("cover url", ""),
                }
                for movie in results[:limit]
            ]

            return movies_data
        except IMDbError as e:
            logging.exception(f"Erreur provenant de IMDb: {e}")
            raise e
        except Exception as e:
            logging.exception(
                f"Erreur inconnue survenue lors de la recherche IMDb: {str(e)}"
            )
            raise RuntimeError("Erreur survenue lors de l'interaction avec IMDb") from e

    def get_movie_details(self, imdb_id: str) -> Dict:
        """
        Récupère les détails complets d'un film selon son ID IMDb.

        Args:
            imdb_id (str): L'identifiant IMDb du film.

        Returns:
            Dict: Détails du film sous forme de dictionnaire.

        Raises:
            IMDbError: Si une erreur se produit avec l'API IMDb.
            RuntimeError: Pour d'autres erreurs lors de la récupération des détails.
        """
        try:
            # movie = web.get_title(imdb_id)
            movie = get_movie(imdb_id)

            return {
                "imdb_id": imdb_id,
                "title": getattr(movie, "title", "N/A"),
                "duration": self.format_runtime(getattr(movie, "duration", "N/A")),
                "summary": getattr(movie, "plot", "N/A"),
                "poster_url": getattr(movie, "cover_url", "N/A"),
                "directors": self._extract_people(getattr(movie, "directors", [])),
                "producers": self._extract_people(getattr(movie, "producers", [])),
                "actors": self._extract_people(getattr(movie, "stars", [])[:10]),
                "categories": [
                    {"name": genre} for genre in getattr(movie, "genres", [])
                ],
            }

        except Exception as e:
            logging.exception(
                f"Erreur lors de la récupération des détails du film (IMDb Id: {imdb_id})."
            )
            raise RuntimeError(
                "Erreur lors de la récupération des détails du film"
            ) from e

    def format_runtime(self, runtime):
        """
        Formate la durée d'un film.

        Args:
            runtime (int | str): La durée du film en minutes.

        Returns:
            str: La durée formatée en heures et minutes ("hh:mm").
        """

        try:
            q = int(runtime) // 60
            r = int(runtime) % 60
            return f"{q}h{r}"
        except Exception as e:
            logging.warning(f"Erreur dans le calcul du runtime ({e})", exc_info=True)
            return "N/A"

    def _extract_people(self, people) -> List[Dict]:
        """
        Extrait une liste d'individus (réalisateurs, producteurs, acteurs).

        Args:
            people: Liste d'objets personnes récupérés de l'API IMDb.

        Returns:
            List[Dict]: Liste de dictionnaires contenant le nom et l'ID IMDb des personnes.
        """

        return [
            {
                "name": getattr(person, "name", "N/A"),
                "imdb_id": getattr(person, "imdbId", "N/A"),
            }
            for person in people
        ]
