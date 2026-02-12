import random
import movie_storage_sql as db


def print_helper(movies):
    if isinstance(movies, tuple):
        print(f"{movies[0]}, {movies[1]['year']}, {movies[1]['rating']}")

    if isinstance(movies, dict):
        for key, val in movies.items():
            print(f"{key}, {val['year']}, {val['rating']}")

    if isinstance(movies, list) and len(movies) < 2:
        print(f"{movies[0][0]}, {movies[0][1]}, {movies[0][2]}")


def header(text):
    stars = "*" * 5
    print(f"\n{stars} {text} {stars}")


def command_calc_median(movies):
    movies = list(movies.values())
    movies_length = len(movies)

    if movies_length % 2 == 1:
        return movies[movies_length // 2]['rating']
    else:
        middle1 = movies[movies_length // 2 - 1]['rating']
        middle2 = movies[movies_length // 2]['rating']
        return (middle1 + middle2) / 2


def command_search_movie():
    header("Search a movie")
    query = input("Enter part of movie name: ")

    if not isinstance(query, str):
        print("Please enter a string!")
        return None

    print_helper(db.search_movie(query))
    return None


def command_delete_movie(title):
    header("Delete a movie")

    movie_name = input("Enter the name of a movie you want to delete: ")

    if movie_name == title:
        db.delete_movie(title)
    else:
        print("\nThe movie you want to delete is not available!\n")


def command_list_movies(movies):
    header(f"{len(movies)} movies in total")
    print_helper(movies)


def command_add_movie():
    header("Add a new movie")

    movie_name = input("Enter movie name: ")
    movie_rating = float(input("Enter movie rating: "))
    movie_year = int(input("Enter movie year: "))

    if 1 <= movie_rating <= 10:
        db.add_movie(movie_name, movie_year, movie_rating)
    else:
        print("Movie rating must be between 1 and 10! Try again...")


def command_update_movie(movies):
    header("Update a movie")

    movie_name = input("Enter the name of a movie you want to update: ")

    if movie_name in movies:
        movie_rating = float(input("Enter the new rating for the movie: "))
        db.update_movie(movie_name, movie_rating)
    else:
        print("\nThe movie you want to update is not available!\n")


def sort_movies_by_rating(movies):
    header("Sort the movies by rating")
    for key, val in sorted(movies.items(), key=lambda item: item[1], reverse=True):
        print_helper(key, val)


def random_movie(movies):
    header("Random movie")
    movie = random.choice(list(movies.items()))
    print_helper(movie)


def stats(movies):
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
    movies = db.list_movies()

    while True:
        header("My Movies Database")
        print(
            "Menu:\n0. Exit\n1. List movies\n2. Add movie\n3. Delete movie\n4. Update movie\n5. Stats\n6. Random movie\n7. Search movie\n8. Movies sorted by rating")

        user_input = input("Enter choice (0-8): ")

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
        elif user_input == "0":
            print("Bye!")
            break
        else:
            print("Invalid input! Try again...")

        input("\nPress enter to continue")


if __name__ == "__main__":
    try:
        main()
    # print some nice message when quitting the program using keyboard interrupt
    except KeyboardInterrupt:
        print("See ya!")