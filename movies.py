import random


def header(text):
    stars = "*" * 5
    print(f"\n{stars} {text} {stars}")


def calc_median(movies):
    movies = list(movies.values())
    movies.sort()
    movies_length = len(movies)
    if movies_length % 2 == 1:
        return movies[movies_length // 2]
    else:
        middle1 = movies[movies_length // 2 - 1]
        middle2 = movies[movies_length // 2]
        return (middle1 + middle2) / 2


def search_movie(movies):
    header("Search a movie")
    query = input("Enter part of movie name: ")

    if type(query) != str:
        print("Please enter a string!")
        return None

    for key, val in movies.items():
        if query.lower() in key.lower():
            print(f"{key}, {val}")
    return None


def delete_movie(movie):
    header("Delete a movie")

    movie_name = input("Enter the name of a movie you want to delete: ")

    if movie_name in movie:
        del movie[movie_name]
        print("\nMovie deleted!\n")
    else:
        print("\nThe movie you want to delete is not available!\n")


def list_movies(movies):
    header(f"{len(movies)} movies in total")

    for key, val in movies.items():
        print(f"{key}: {val}")


def add_movie(movies):
    header("Add a new movie")

    movie_name = input("Enter movie name: ")
    movie_rating = float(input("Enter movie rating: "))

    if 1 <= movie_rating <= 10:
        movies[movie_name] = movie_rating
        print("\nMovie added!\n")
    else:
        print("Movie rating must be between 1 and 10! Try again...")


def update_movie(movies):
    header("Update a movie")

    movie_name = input("Enter the name of a movie you want to update: ")

    if movie_name in movies:
        movie_rating = float(input("Enter the new rating for the movie: "))
        movies[movie_name] = movie_rating
        print("\nMovie updated!\n")
    else:
        print("\nThe movie you want to update is not available!\n")


def sort_movies_by_rating(movies):
    header("Sort the movies by rating")
    for key, val in sorted(movies.items(), key=lambda item: item[1], reverse=True):
        print(f"{key}, {val}")


def random_movie(movies):
    header("Random movie")
    movie = random.choice(list(movies.items()))
    print(f"{movie[0]}, {movie[1]}")


def stats(movies):
    lowest = min(movies.values())
    highest = max(movies.values())

    header("Movie stats")

    print("\n1. Average rating =>", "%.1f" % (sum(movies.values()) / len(movies)))
    print("2. Median of ratings =>", calc_median(movies))

    worst_movies = {}
    best_movies = {}

    for key, val in movies.items():
        if val == lowest:
            worst_movies[key] = val
        elif val == highest:
            best_movies[key] = val

    if best_movies:
        print("3. Best movie(s) =>")
        for key, val in best_movies.items():
            print(f"{key}: {val}")

    if worst_movies:
        print("4. Worst movie(s) =>")
        for key, val in worst_movies.items():
            print(f"{key}: {val}")


def main():
    movies = {
        "The Shawshank Redemption": 9.5,
        "Pulp Fiction": 8.8,
        "The Room": 3.6,
        "The Godfather": 9.2,
        "The Godfather: Part II": 9.0,
        "The Dark Knight 2": 3.6,
        "12 Angry Men": 8.9,
        "The Dark Knight": 9.0,
        "Everything Everywhere All At Once": 8.9,
        "Forrest Gump": 8.8,
        "Star Wars: Episode V": 8.7,
    }

    while True:
        header("My Movies Database")
        print(
            "Menu:\n1. List movies\n2. Add movie\n3. Delete movie\n4. Update movie\n5. Stats\n6. Random movie\n7. Search movie\n8. Movies sorted by rating")

        user_input = input("Enter choice (1-8 or press 'q' to quit): ")

        if user_input == "1":
            list_movies(movies)
        elif user_input == "2":
            add_movie(movies)
        elif user_input == "3":
            delete_movie(movies)
        elif user_input == "4":
            update_movie(movies)
        elif user_input == "5":
            stats(movies)
        elif user_input == "6":
            random_movie(movies)
        elif user_input == "7":
            search_movie(movies)
        elif user_input == "8":
            sort_movies_by_rating(movies)
        elif user_input == "q":
            print("See ya!")
            break
        else:
            print("Invalid input! Try again...")

        input("\nPress enter to continue")


if __name__ == "__main__":
    main()
