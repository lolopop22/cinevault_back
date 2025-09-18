import os
import logging
from imdb import Cinemagoer, IMDbError
from imdbinfo.services import get_movie
from typing import List, Dict


class IMDbService:
    def __init__(self):
        self.ia = Cinemagoer()

    def search_movie(
        self, title: str, limit: int = int(os.getenv("SEARCH_FILM_LIMIT"))
    ) -> List[Dict]:
        """Recherche des films sur IMDb"""
        logging.info(f"Recherche du film {title}")

        try:
            results = self.ia.search_movie(title)
            movies_data = []

            for movie in results[:limit]:
                movies_data.append(
                    {
                        "imdb_id": movie.movieID,
                        "title": movie.get("title", ""),
                        "poster_url": movie.get("cover url", ""),
                    }
                )
            return movies_data
        except IMDbError as e:
            logging.exception(f"Erreur provenant de IMDb: {e}")
            raise e
        except Exception as e:
            logging.exception(
                f"Erreur inconnue survenue lors de la recherche IMDb: {str(e)}"
            )
            raise Exception(
                f"Erreur inconnue survenue lors de la recherche IMDb: {str(e)}"
            )

    def get_movie_details(self, imdb_id: str) -> Dict:
        """Obtient les détails complets d'un film selon IMDb ID."""
        try:
            # movie = web.get_title(imdb_id)
            movie = get_movie(imdb_id)

            title = getattr(movie, "title", "N/A")
            duration = self.format_runtime(getattr(movie, "duration", "N/A"))
            summary = getattr(movie, "plot", "N/A")
            poster_url = getattr(movie, "cover_url", "N/A")
            directors = getattr(movie, "directors", "N/A")
            producers = getattr(movie, "producers", "N/A")
            actors = getattr(movie, "stars", "N/A")

            logging.debug(f"movie: {title}")
            logging.debug(f"runtime: {duration}")
            logging.debug(f"summary: {summary}")
            logging.debug(f"poster_url: {poster_url}")
            logging.debug(f"actors: {actors}")
            logging.debug(f"producers: {producers}")
            logging.debug(f"directors: {directors}")

            return {
                "imdb_id": imdb_id,
                "title": title,
                "duration": duration,
                "summary": summary,
                "poster_url": poster_url,
                "directors": self._extract_people(directors),
                "producers": self._extract_people(producers),
                "actors": self._extract_people(actors)[:10],
            }
        except Exception as e:
            logging.exception(
                f"Erreur lors de la récupération des détails du film (IMDb Id: {imdb_id})."
            )
            raise Exception(
                f"Erreur lors de la récupération des détails du film avec l'id IMDb {imdb_id} : {str(e)}"
            )

    def format_runtime(self, runtime):
        try:
            q = int(runtime) // 60
            r = int(runtime) % 60
            return f"{q}h{r}"
        except Exception as e:
            logging.warning(f"Erreur dans le calcul du runtime ({e})", exc_info=True)
            return "N/A"

    def _extract_people(self, people) -> List[Dict]:
        """Extrait une liste de personnes (réalisateurs, producteurs, acteurs)."""
        return [
            {
                "name": getattr(person, "name", "N/A"),
                "imdb_id": getattr(person, "imdbId", "N/A"),
            }
            for person in people
        ]
