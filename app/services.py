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
        """Récupère les détails complets d'un film"""
        try:
            movie = self.ia.get_movie(
                imdb_id,
                info=(
                    "title",
                    "runtime",
                    "plot",
                    "cover",
                    "directors",
                    "producers",
                    "cast",
                ),
            )

            logging.debug(f"runtime: {movie.get('runtime')}")
            logging.debug(f"movie: {movie.data}")
            # logging.debug(f"actors: {movie['cast']}
            logging.debug(f"producers: {movie['producer']}")
            logging.debug(f"directors: {movie['director']}")

            return {
                "imdb_id": imdb_id,
                "title": movie.get("title", ""),
                "duration": (
                    self.runtime_str(movie.get("runtime")[0])
                    if movie.get("runtime")
                    else "Non indiqué"
                ),
                "summary": movie.get("plot", [""])[0] if movie.get("plot") else "",
                "poster_url": movie.get("cover url", "Non indiqué"),
                # "categories": [genre for genre in movie.get("genres", [])],
                "directors": [
                    director["name"] for director in movie.get("directors", [])
                ],
                "producers": [
                    producer["name"] for producer in movie.get("producers", [])
                ],
                "actors": [actor["name"] for actor in movie.get("cast", [])[:10]],
            }
        except IMDbError as e:
            logging.exception(f"Erreur provenant de IMDb: {e}")
            raise e
        except Exception as e:
            raise Exception(
                f"Erreur lors de la récupération des détails du film avec l'id IMDb {imdb_id} : {str(e)}"
            )

    def runtime_str(self, runtime):
        try:
            q = int(runtime) // 60
            r = int(runtime) % 60
            return f"{q}h{r}"
        except Exception as e:
            logging.warning(f"Erreur dans le calcul du runtime ({e})", exc_info=True)
            return "Non indiqué"
