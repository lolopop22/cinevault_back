import os
import logging
from imdb import Cinemagoer, IMDbError
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
                        "title": movie.get("title", "Non indiqué"),
                        "poster_url": movie.get("cover url", "Non indiqué"),
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
