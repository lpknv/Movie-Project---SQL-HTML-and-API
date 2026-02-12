import random
import movie_storage_sql as db


def print_helper(data):
    """Helper function for printing movie data"""

    # title, year, rating = None, None, None
    print(f"{'Title':<26} {'Year':<5} {'Rating'}")
    print("-" * 36)

    def _print(title, year, rating):
        print(f"{title:<26} {year:<5} {rating}")

    if isinstance(data, tuple):
        _print(data[0], data[1]['year'], data[1]['rating'])
    elif isinstance(data, dict):
        for key, val in data.items():
            _print(key, val['year'], val['rating'])
    elif isinstance(data, list):
        if len(data) > 1:
            for item in data:
                _print(item[0], item[1]['year'], item[1]['rating'])
        else:
            item = data[0]
            _print(item[0], item[1], item[2])
    else:
        print(data)


def header(text):
    """Helper function for printing header text"""
    stars = "*" * 5
    print(f"\n{stars} {text} {stars}")


def command_calc_median(movies):
    """Calculate the median of all movies"""

    movie_list = sorted(movies.values(), key=lambda x: x['rating'])
    movies_length = len(movie_list)

    if movies_length % 2 == 1:
        return movie_list[movies_length // 2]['rating']

    else:
        middle1 = movie_list[movies_length // 2 - 1]['rating']
        middle2 = movie_list[movies_length // 2]['rating']
        return (middle1 + middle2) / 2


def command_search_movie():
    """Search a movie"""
    header("Search a movie")
    query = input("Enter part of movie name: ")

    if not isinstance(query, str):
        print("Please enter a string!")
        return None

    print_helper(db.search_movie(query))
    return None


def command_delete_movie(movies):
    """Delete a movie by title"""
    header("Delete a movie")
    command_list_movies(movies)
    movie_name = input("\nEnter the name of a movie you want to delete: ")

    if movie_name in movies.keys():
        db.delete_movie(movie_name)
    else:
        print("\nThe movie you want to delete is not available!\n")


def command_list_movies(movies):
    """Print all movies"""
    header(f"{len(movies)} movies in total")
    print_helper(movies)


def command_add_movie():
    """Add a new movie to the database"""
    header("Add a new movie")

    movie_name = input("Enter movie name: ")
    movie_rating = int(input("Enter movie rating: "))
    movie_year = int(input("Enter movie year: "))

    if 1 <= movie_rating <= 10:
        db.add_movie(movie_name, movie_year, movie_rating)
    else:
        print("Movie rating must be between 1 and 10! Try again...")


def command_update_movie(movies):
    """Update a movie"""
    header("Update a movie")
    command_list_movies(movies)
    movie_name = input("\nEnter the name of a movie you want to update: ")

    if movie_name in movies:
        try:
            movie_rating = int(input("Enter the new rating for the movie: "))
            movie_year = int(input("Enter the new year for the movie: "))
            db.update_movie(movie_name, movie_year, movie_rating)
        except ValueError as e:
            print(e, "Try again!")
        except TypeError as e:
            print(e, "Try again!")
    else:
        print("\nThe movie you want to update is not available!\n")


def sort_movies_by_rating(movies):
    """Sort movies by rating"""
    header("Sort the movies by rating")
    print_helper(sorted(movies.items(), key=lambda item: item[1]['rating'], reverse=True))


def random_movie(movies):
    """Get a random movie"""
    header("Random movie")
    movie = random.choice(list(movies.items()))
    print_helper(movie)


def stats(movies):
    """Print movie stats"""
    lowest = min(movies)
    highest = max(movies)

    sum_ratings = sum([movie[1]['rating'] for movie in movies.items()])

    header("Movie stats")

    print("\n1. Average rating =>", "%.1f" % (sum_ratings / len(movies)))
    print("2. Median of ratings =>", command_calc_median(movies))

    worst_movies = {}
    best_movies = {}

    for key, val in movies.items():
        if val == lowest:
            worst_movies[key] = val
        elif val == highest:
            best_movies[key] = val

    if best_movies:
        print("3. Best movie(s) =>")
        print_helper(best_movies)

    if worst_movies:
        print("4. Worst movie(s) =>")
        print_helper(worst_movies)


def main():
    """Show movies from database, let user pick options to execute on the movies"""

    while True:
        movies = db.list_movies()

        header("My Movies Database")
        print(
            "Menu:\n0. Exit\n1. List movies\n2. Add movie\n3. Delete movie\n4. Update movie\n5. Stats\n6. Random movie\n7. Search movie\n8. Movies sorted by rating")

        user_input = input("Enter choice (0-8): ")

        if user_input == "0":
            print("Bye!")
            break
        if user_input == "1":
            command_list_movies(movies)
        elif user_input == "2":
            command_add_movie()
        elif user_input == "3":
            command_delete_movie(movies)
        elif user_input == "4":
            command_update_movie(movies)
        elif user_input == "5":
            stats(movies)
        elif user_input == "6":
            random_movie(movies)
        elif user_input == "7":
            command_search_movie()
        elif user_input == "8":
            sort_movies_by_rating(movies)
        else:
            print("Invalid input! Try again...")

        input("\nPress enter to continue")


if __name__ == "__main__":
    try:
        main()
    # print some nice message when quitting the program using keyboard interrupt
    except KeyboardInterrupt:
        print("See ya!")