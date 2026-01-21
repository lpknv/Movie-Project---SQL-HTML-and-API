from sqlalchemy import create_engine, text

# Define the database URL
DB_URL = "sqlite:///movies.db"

# SQL queries
QUERY_CREATE_TABLE_MOVIES_IF_NOT_EXISTS = """
create table IF not exists movies
(
  id integer primary key AUTOINCREMENT,
  title TEXT unique not null,
  year integer not null,
  rating real not null
);
"""
QUERY_ALL_MOVIES = "select title, year, rating from movies"
QUERY_INSERT_NEW_MOVIE = "insert into movies (title, year, rating) values (:title, :year, :rating)"
QUERY_DELETE_MOVIE_BY_TITLE = "delete from movies where title = :title"
QUERY_SEARCH_MOVIE_BY_TITLE = "select title, year, rating from movies where title = :title"
QUERY_UPDATE_MOVIE = "update movies set rating = :rating where title = :title"

# Create the engine
engine = create_engine(DB_URL, echo=(True if __debug__ else False))

# Create the movies table if it does not exist
with engine.connect() as connection:
    connection.execute(text(QUERY_CREATE_TABLE_MOVIES_IF_NOT_EXISTS))
    connection.commit()


def execute_query(query, params=None, commit=False, return_result=False):
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
    movies = execute_query(QUERY_ALL_MOVIES, return_result=True)

    return {row[0]: {"year": row[1], "rating": row[2]} for row in movies}


def add_movie(title, year, rating):
    """Add a new movie to the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text(QUERY_INSERT_NEW_MOVIE),
                               {"title": title, "year": year, "rating": rating})
            connection.commit()
            print(f"Movie '{title}' added successfully.")
        except Exception as e:
            print(f"Error: {e}")


def delete_movie(title):
    """Delete a movie from the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text(QUERY_DELETE_MOVIE_BY_TITLE),
                               {"title": title})
            connection.commit()
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

    # with engine.connect() as connection:
    #     try:
    #         connection.execute(text(QUERY_UPDATE_MOVIE),
    #                            {"title": title, "rating": rating})
    #         connection.commit()
    #         print(f"Movie '{title}' updated successfully.")
    #     except Exception as e:
    #         print(f"Error: {e}")


def search_movie(title):
    """Search for a movie by title in the database."""
    try:
        return execute_query(QUERY_SEARCH_MOVIE_BY_TITLE, {"title": title}, return_result=True)
    except Exception as e:
        print(f"Movie with title '{title}' not found!")
        print(f"Error: {e}")