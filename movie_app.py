import random
import matplotlib.pyplot as plt
import os


class MovieApp:
    def __init__(self, storage):
        self._storage = storage

    def menu(self):
        """prints out the menu for the user to choose from and returns the choice"""
        print("""
        Menu:
        0. Exit
        1. List movies
        2. Add movie
        3. Delete movie
        4. Update movie
        5. Stats
        6. Random movie
        7. Search movie
        8. Movies sorted by rating
        9. Create Rating Histogram
        10. Generate website
        """)

        while True:
            user_choice = input("Enter choice (0-10): ")
            try:
                user_choice = int(user_choice)
                if 0 <= user_choice <= 10:
                    return user_choice
                else:
                    print("Invalid choice. Please enter a number between 0 and 10.")
            except ValueError:
                print("Invalid input. Please enter a number between 0 and 10.")

    def _command_exit_func(self):
        """ prints out "bye!" and exits """
        print("bye!")
        exit()

    def _command_list_movies(self):
        """ Prints a list of all the movies in the movies database """
        # Get the data from the JSON file
        movies = self._storage.list_movies()
        num_of_movies_in_data_base = len(movies)
        print(f"{num_of_movies_in_data_base} movies in total")
        for movie_name, movie_info in movies.items():
            release_year = movie_info['release_year']
            rating = movie_info['rating']
            notes = movie_info.get('notes')
            movie_details = f"{movie_name} ({release_year}) : {rating} "
            if notes:
                movie_details += f"(notes: {notes})"
            print(movie_details)

    def _command_add_movie(self):
        """ Adds a movie to the movies database """
        # Get the data from the JSON file
        movies = self._storage.list_movies()
        title = input("Enter new movie name: ")
        if title in movies:
            print(f"Movie {title} already exist!")
        elif self._storage.fetch_movie_info(title) is None:
            print("there was a problem fetching movie info")
        else:
            # Add the movie and save the data to the JSON file
            new_title = self._storage.fetch_movie_info(title)[0]
            year = self._storage.fetch_movie_info(title)[1]
            rating = self._storage.fetch_movie_info(title)[2]
            poster = self._storage.fetch_movie_info(title)[3]
            self._storage.add_movie(new_title, year, rating, poster)
            print(f"Movie {title} successfully added")
        return movies

    def _command_del_movie(self):
        """ Allowing the user to delete a movie from database """
        # Get the data from the JSON file
        movies = self._storage.list_movies()
        title = input("Enter movie name to delete: ")
        self._storage.delete_movie(title)
        return movies

    def _command_update_movie(self):
        """ Allowing the user to update a movie in the database """
        # Get the data from the JSON file
        movies = self._storage.list_movies()
        title = input("Enter movie name: ")
        notes = input("Please write notes: ")
        self._storage.update_movie(title, notes)
        return movies

    def _command_movie_stats(self):
        """ printing average rating, median rating, best movie and worst movie in database """
        # Get the data from the JSON file
        movies = self._storage.list_movies()
        num_of_movies = len(movies)
        list_of_ratings = []
        for movie_info in movies.values():
            list_of_ratings.append(float(movie_info["rating"]))

        def average(num_of_movies, list_of_ratings):
            average_rating = (float(sum(list_of_ratings)) / num_of_movies)
            print(f"Average rating: {average_rating}")

        def median(num_of_movies, list_of_ratings):
            sorted_list_of_ratings = sorted(list_of_ratings)
            if num_of_movies % 2 == 0:
                location_of_median1 = int(num_of_movies / 2)
                location_of_median2 = int(location_of_median1 - 1)
                median = (((sorted_list_of_ratings[location_of_median1]) + (
                    sorted_list_of_ratings[location_of_median2])) / 2)
            else:
                location_of_median = int(num_of_movies / 2 - 0.5)
                median = sorted_list_of_ratings[location_of_median]
            print(f"Median rating: {median}")

        def best_and_worst_movies(movies):
            max_rating = -float("inf")
            max_rating_movie = None
            min_rating = float("inf")
            min_rating_movie = None
            for movie_name, movie_info in movies.items():
                if float(movie_info['rating']) > max_rating:
                    max_rating = float(movie_info['rating'])
                    max_rating_movie = movie_name
                if float(movie_info['rating']) < min_rating:
                    min_rating = float(movie_info['rating'])
                    min_rating_movie = movie_name
            print(f"Best movie: {max_rating_movie}, {max_rating}")
            print(f"Worst movie: {min_rating_movie}, {min_rating}")

        average(num_of_movies, list_of_ratings)
        median(num_of_movies, list_of_ratings)
        best_and_worst_movies(movies)

    def _command_random_movie(self):
        """ printing a random movie and its rating from database """
        # Get the data from the JSON file
        movies = self._storage.list_movies()
        movie_names = list(movies.keys())
        random_movie_name = random.choice(movie_names)
        print(random_movie_name, movies[random_movie_name]["rating"])

    def _command_search_movie(self):
        """ Searching for a movie in the database (case-insensitive). """
        # Get the data from the JSON file
        movies = self._storage.list_movies()
        part_of_name = input("Enter part of movie name: ")
        movie_found = False  # Flag variable to track if a movie is found

        for movie_name, movie_info in movies.items():
            if part_of_name.lower() in movie_name.lower():
                movie_rating = movies[movie_name]["rating"]
                print(f"{movie_name}, {movie_rating}")
                movie_found = True

        if not movie_found:
            print("Movie not found")

    def _command_sorted_by_rating(self):
        """
        Displays the movies sorted by rating in descending order.
        """
        movies = self._storage.list_movies()
        sorted_movies = sorted(movies.items(), key=lambda x: x[1]["rating"], reverse=True)
        for movie in sorted_movies:
            print(f"{movie[0]} ({movie[1]['release_year']}) - {movie[1]['rating']}")

    def _command_create_rating_histogram(self):
        """ create a histogram of the ratings in database"""
        # Get the data from the JSON file
        movies = self._storage.list_movies()
        x = []
        for movie_name, movie_info in movies.items():
            x.append(movie_info["rating"])
        plt.hist(x, len(movies), facecolor="pink", edgecolor="black", rwidth=0.9)
        plt.xlabel("Movie rating")
        plt.ylabel("Frequency")
        plt.title("Movies rating Histogram")
        file_name = input("Save histogram under what file name: ")
        plt.savefig(f"{file_name}.png")
        plt.show()

    def _command_generate_website(self):
        """ create a website from the movie in database"""
        # Get the data from the JSON file
        movies = self._storage.list_movies()

        def read_html_template_to_file():
            with open("index_template.html", "r") as fileobj:
                html_template = fileobj.read()
            return html_template

        def create_string_for_html(movies):
            """ creating a string from all relevant info about the movies.
            the string will be used later as the body of the HTML file. """
            output_as_string = ""
            if movies:
                for movie_name in movies:
                    output_as_string += '<li><div class="movie">'
                    movie_poster_url = movies[movie_name]["poster"]
                    output_as_string += f'<img class="movie-poster" src="{movie_poster_url}"/>'
                    output_as_string += f'<div class="movie-title">{movie_name}</div>'
                    movie_year = movies[movie_name]["release_year"]
                    output_as_string += f'<div class="movie-year">{movie_year}</div>'
                    output_as_string += '</div></li>'
            else:
                output_as_string += "<h2>No movies in database</h2>"
            return output_as_string

        output_as_string = create_string_for_html(movies)
        html_template = read_html_template_to_file()
        new_html_data = html_template.replace("__TEMPLATE_MOVIE_GRID__", output_as_string)
        # Get the name of the JSON file (without the extension)
        json_file_name = os.path.splitext(self._storage.file_path)[0]
        # Set the HTML filename based on the JSON file name
        html_filename = json_file_name + ".html"
        with open(html_filename, "w") as moviefile:
            moviefile.write(new_html_data)
        print("Website was generated successfully.")

    def run(self):
        """Starts the movie app and handles user commands"""
        while True:
            choice = self.menu()
            if choice == 0:
                self._command_exit_func()
            elif choice == 1:
                self._command_list_movies()
            elif choice == 2:
                self._command_add_movie()
            elif choice == 3:
                self._command_del_movie()
            elif choice == 4:
                self._command_update_movie()
            elif choice == 5:
                self._command_movie_stats()
            elif choice == 6:
                self._command_random_movie()
            elif choice == 7:
                self._command_search_movie()
            elif choice == 8:
                self._command_sorted_by_rating()
            elif choice == 9:
                self._command_create_rating_histogram()
            elif choice == 10:
                self._command_generate_website()
            else:
                print("Invalid choice. Please try again.\n")
