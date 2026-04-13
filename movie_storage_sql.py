from sqlalchemy import create_engine, text

from omdb_api import search_movie_by_title

# Define the database URL
DB_URL = "sqlite:///movies.db"

# SQL queries
QUERY_CREATE_TABLE_MOVIES_IF_NOT_EXISTS = """
create table IF not exists movies
(
  id integer primary key AUTOINCREMENT,
  title TEXT unique not null,
  year integer not null,
  rating real not null,
  poster_image_url TEXT null
);
"""
QUERY_ALL_MOVIES = "select title, year, rating, poster_image_url from movies"
QUERY_INSERT_NEW_MOVIE = "insert into movies (title, year, rating, poster_image_url) values (:title, :year, :rating, :poster_image_url)"
QUERY_DELETE_MOVIE_BY_TITLE = "delete from movies where title = :title"
QUERY_SEARCH_MOVIE_BY_TITLE = "select title, year, rating, poster_image_url from movies where lower(title) like lower(:title)"
QUERY_UPDATE_MOVIE = "update movies set rating = :rating where title = :title"

# Create the engine
engine = create_engine(DB_URL, echo=(True if __debug__ else False))

# Create the movies table if it does not exist
with engine.connect() as connection:
    connection.execute(text(QUERY_CREATE_TABLE_MOVIES_IF_NOT_EXISTS))
    connection.commit()


def execute_query(query, params=None, commit=False, return_result=False):
    """Execute SQL query helper function"""
    with engine.connect() as conn:
        try:
            result = conn.execute(text(query), params or {})

            if commit:
                conn.commit()
            if return_result:
                return result.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            return None

    return None


def list_movies():
    """Retrieve all movies from the database."""
    movies = execute_query(QUERY_ALL_MOVIES, return_result=True) or []

    return {row[0]: {"year": row[1], "rating": row[2], "poster_image_url": row[3]} for row in movies}


def add_movie(title):
    """
    Fetch movie by title using the OMDB API (title, year, rating, poster url)
    Add a new movie to the database, if movie was found.
    """
    movie = search_movie_by_title(title)

    if not movie or movie.get("error"):
        print(f"Movie not added: {movie.get('error', 'Movie not found')}")
        return False

    try:
        execute_query(
            QUERY_INSERT_NEW_MOVIE,
            {
                "title":            movie.get("title"),
                "year":             movie.get("year"),
                "rating":           movie.get("rating"),
                "poster_image_url": movie.get("poster_image_url", ""),
            },
            commit=True,
            return_result=False,
        )
        print(f"Movie '{movie['title']}' added successfully.")
        return True

    except Exception as e:
        # ideally catch DB-specific exceptions here if you know the library
        print(f"Database error while adding '{title}': {e}")
        return False


def delete_movie(title):
    """Delete a movie from the database."""
    try:
        execute_query(QUERY_DELETE_MOVIE_BY_TITLE, {"title": title}, commit=True,
                      return_result=False)
        print(f"Movie '{title}' deleted successfully.")
    except Exception as e:
        print(f"Error: {e}")


def update_movie(title, rating):
    """Update a movie's rating in the database."""
    try:
        execute_query(QUERY_UPDATE_MOVIE, {"title": title, "rating": rating}, commit=True)
        print(f"Movie '{title}' updated successfully.")
    except Exception as e:
        print(f"Error: {e}")


def search_movie(title):
    """Search for a movie by title in the database."""
    try:
        return execute_query(QUERY_SEARCH_MOVIE_BY_TITLE, {"title": title}, return_result=True)
    except Exception as e:
        print(f"Movie with title '{title}' not found!")
        print(f"Error: {e}")