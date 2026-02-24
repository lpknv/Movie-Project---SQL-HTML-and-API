import requests

import os
from dotenv import load_dotenv

load_dotenv()  # loads variables from .env

API_URL = "https://www.omdbapi.com/"
API_KEY = os.getenv("OMDB_API_KEY")


def search_movie_by_title(title):
    try:
        response = requests.get(API_URL, params={
            "apikey": API_KEY,
            "t":      title
        })

        response.raise_for_status()

        movie = response.json()

        if movie.get("Response") == "False":
            return {
                "error": movie.get("Error", "Unknown API error")
            }

        return {
            "title":            movie.get("Title"),
            "year":             movie.get("Year"),
            "rating":           movie.get("imdbRating"),
            "poster_image_url": movie.get("Poster")
        }

    except requests.exceptions.RequestException as e:
        return {
            "error": f"Network error: {str(e)}"
        }
    except ValueError:
        return {
            "error": "Invalid JSON response from API"
        }