from istorage import IStorage
import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from the .env file

MY_KEY = os.getenv("API_KEY")
REQUEST_URL = os.getenv("REQUEST_URL")


class StorageJson(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path

    def list_movies(self):
        """
        Returns a dictionary of dictionaries that
        contains the movies information in the database.

        The function loads the information from the JSON
        file and returns the data.
        If the JSON file does not exist- it creates an empty one.

        For example, the function may return:
        {
          "Titanic": {
            "rating": 9,
            "year": 1999
          },
          "..." {
            ...
          },
        }
        """
        if not os.path.exists(self.file_path):
            # If the file doesn't exist, create an empty JSON object
            with open(self.file_path, "w") as file:
                json.dump({}, file)

        with open(self.file_path, "r") as fileobj:
            movies_data = json.loads(fileobj.read())
        return movies_data

    # fetching movie info from API
    def fetch_movie_info(self, title):
        """ Fetching the movie info from the API """
        try:
            res = requests.get(REQUEST_URL, params={"t": title, "apikey": MY_KEY})
            if res.status_code == 200:
                movie_data = res.json()
                if movie_data["Response"] == "False":
                    return None
                title = movie_data["Title"]
                year = movie_data["Year"]
                rating = movie_data["imdbRating"]
                poster = movie_data["Poster"]
                return title, year, rating, poster
            else:
                return None
        except requests.exceptions.RequestException:
            return None

    def add_movie(self, title, year, rating, poster):
        """
        Adds a movie to the movies database.
        Loads the information from the JSON file, add the movie,
        and saves it. The function doesn't need to validate the input.
        """
        with open(self.file_path, "r") as fileobj:
            movies_data = json.loads(fileobj.read())
        movies_data[title] = {
            "name": title,
            "rating": rating,
            "release_year": year,
            "poster": poster,
            "notes": []
        }
        with open(self.file_path, "w") as newfile:
            json.dump(movies_data, newfile, indent=4)

    def delete_movie(self, title):
        """
        Deletes a movie from the movies database.
        Loads the information from the JSON file, deletes the movie,
        and saves it. The function doesn't need to validate the input.
        """
        with open(self.file_path, "r") as fileobj:
            movies_data = json.loads(fileobj.read())
        if title in movies_data:
            del movies_data[title]
            print(f"Movie {title} successfully deleted")
        else:
            print(f"Movie {title} doesn't exist!")
        with open(self.file_path, "w") as newfile:
            json.dump(movies_data, newfile, indent=4)

    def update_movie(self, title, notes):
        """ Adds notes to the movie data """
        with open(self.file_path, "r") as fileobj:
            movies_data = json.loads(fileobj.read())
        if title in movies_data:
            movies_data[title]["notes"] = notes
            print(f"Movie {title} successfully updated")
        else:
            print(f"Movie {title} doesn't exist!")
        with open(self.file_path, "w") as newfile:
            json.dump(movies_data, newfile, indent=4)
