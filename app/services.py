from imdb import Cinemagoer, IMDbError, Movie
from typing import List, Dict


class IMDbService:
    def __init__(self):
        self.ia = Cinemagoer()

    def search_movie(self, title: str, limit: int = 10) -> List[Dict]:
        """Recherche des films sur IMDb"""

        try:
            results = self.ia.search_movie(title)
            movies_data = []

            for movie in results[:limit]:
                movies_data.append(
                    {
                        "imdb_id": movie.movieID,
                        "title": movie["title"],
                        "poster_url": movie["cover url"],
                    }
                )

            return movies_data
        except IMDbError as e:
            print(e)
            raise e
        except Exception as e:
            raise Exception(
                f"Erreur inconnue survenue lors de la recherche IMDb: {str(e)}"
            )
