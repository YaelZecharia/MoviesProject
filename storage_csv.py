from istorage import IStorage
import requests
import os
from dotenv import load_dotenv
import csv

load_dotenv()  # Load environment variables from the .env file

MY_KEY = os.getenv("API_KEY")
REQUEST_URL = os.getenv("REQUEST_URL")


class StorageCsv(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path

    def list_movies(self):
        """
        Returns a dictionary of dictionaries that contains the movies information in the database.
        The function loads the information from the CSV file and returns the data.
        If the file does not exist, it creates an empty one.

        For example, the function may return:
        {
            "Titanic": {
                "rating": 9,
                "release_year": 1999,
                "poster": "http://example.com/poster.jpg",
                "notes": "..."
            },
            "...": {
                ...
            },
        }
        """
        if not os.path.exists(self.file_path):
            # If the file doesn't exist, create an empty CSV file with the required headers
            with open(self.file_path, "w", newline="") as file:
                fieldnames = ["title", "release_year", "rating", "poster", "notes"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()

        movies_data = {}
        with open(self.file_path, "r", newline="") as fileobj:
            reader = csv.DictReader(fileobj)
            for row in reader:
                title = row.get("title")
                rating = float(row.get("rating"))
                release_year = int(row.get("release_year"))
                poster = row.get("poster")
                notes = row.get("notes")
                if title:
                    movies_data[title] = {
                        "rating": rating,
                        "release_year": release_year,
                        "poster": poster,
                        "notes": notes
                    }
        return movies_data

    # fetching movie info from API
    def fetch_movie_info(self, title):
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
        Loads the information from the CSV file, add the movie,
        and saves it. The function doesn't need to validate the input.
        """
        fieldnames = ["title", "release_year", "rating", "poster", "notes"]
        movie_data = {
            "title": title,
            "release_year": year,
            "rating": rating,
            "poster": poster,
            "notes": ""
        }
        with open(self.file_path, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(movie_data)

    def delete_movie(self, title):
        """
        Deletes a movie from the movies database.
        Loads the information from the JSON file, deletes the movie,
        and saves it. The function doesn't need to validate the input.
        """
        movies_data = []
        with open(self.file_path, "r", newline="") as fileobj:
            reader = csv.DictReader(fileobj)
            fieldnames = reader.fieldnames
            movies_data.append(fieldnames)

            for row in reader:
                if row["title"] != title:
                    movies_data.append(row)

        with open(self.file_path, "w", newline="") as fileobj:
            writer = csv.writer(fileobj)
            writer.writerows(movies_data)

        print(f"Movie {title} successfully deleted")

    def update_movie(self, title, notes):
        movies_data = []
        with open(self.file_path, "r", newline="") as fileobj:
            reader = csv.DictReader(fileobj)
            fieldnames = reader.fieldnames
            movies_data.append(fieldnames)

            for row in reader:
                if row["title"] == title:
                    row["notes"] = notes
                movies_data.append(row)
        with open(self.file_path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(movies_data)

        print(f"Movie {title} successfully updated")
