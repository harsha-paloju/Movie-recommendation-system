
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("api_key")

BASE_URL = "https://api.themoviedb.org/3/search/movie"
IMAGE_URL = "https://image.tmdb.org/t/p/w500"


def poster_path(movie_name):

    if not API_KEY:
        print("TMDB API key not found.")
        return None

    params = {
        "api_key": API_KEY,
        "query": movie_name,
        "language": "en-US"
    }

    for attempt in range(3):

        try:
            response = requests.get(
                BASE_URL,
                params=params,
                timeout=15
            )

            if response.status_code == 429 or response.status_code >= 500:
                if attempt < 2:
                    time.sleep(1 + attempt)
                    continue

            response.raise_for_status()

            data = response.json()
            results = data.get("results", [])

            if not results:
                print(f"No TMDB results found for: {movie_name}")
                return None

            
            for movie in results:
                poster = movie.get("poster_path")

                if poster:
                    return f"{IMAGE_URL}{poster}"

            print(f"No poster available for: {movie_name}")
            return None

        except (requests.RequestException, ValueError) as error:

            print(
                f"Attempt {attempt + 1} failed for "
                f"{movie_name}: {error}"
            )

            if attempt < 2:
                time.sleep(1 + attempt)

    return None