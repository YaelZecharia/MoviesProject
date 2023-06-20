from movie_app import MovieApp
from storage_csv import StorageCsv


def main():
    storage = StorageCsv('movies.csv')
    movie_app = MovieApp(storage)
    movie_app.run()


if __name__ == "__main__":
    main()
