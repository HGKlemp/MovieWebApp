import re

import requests


class OMDbAPIError(Exception):
    """Raised when OMDb cannot return usable movie data."""


class MovieNotFoundError(OMDbAPIError):
    """Raised when OMDb cannot find the requested title."""


class OMDbAPI:
    """Fetch and normalize movie information from the OMDb API."""

    BASE_URL = "https://www.omdbapi.com/"

    def __init__(self, api_key):
        self.api_key = api_key

    def fetch_movie(self, title):
        """Return normalized details for one movie title."""
        try:
            response = requests.get(
                self.BASE_URL,
                params={"apikey": self.api_key, "t": title},
                timeout=10,
            )
            response.raise_for_status()
            movie_data = response.json()
        except (requests.RequestException, ValueError) as error:
            raise OMDbAPIError(
                "The movie service is currently unavailable."
            ) from error

        if movie_data.get("Response") == "False":
            raise MovieNotFoundError("Movie not found.")

        year_match = re.search(r"\d{4}", movie_data.get("Year", ""))
        if year_match is None:
            raise OMDbAPIError("The movie service returned an invalid year.")

        poster_url = movie_data.get("Poster", "")
        if poster_url == "N/A":
            poster_url = ""

        director = movie_data.get("Director", "Unknown")
        if director == "N/A":
            director = "Unknown"

        return {
            "name": movie_data.get("Title", title).strip(),
            "director": director,
            "year": int(year_match.group()),
            "poster_url": poster_url,
        }
