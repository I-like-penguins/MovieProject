import os

from sqlalchemy import create_engine, text
ECHO_SQL = True


# Define the database URL
#DB_URL = "sqlite:///movies.db"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Define the database URL to be in the same directory as this script
DB_URL = f"sqlite:///{os.path.join(BASE_DIR, 'movies.db')}"


# Create the engine
engine = create_engine(DB_URL, echo=ECHO_SQL)

# Create the movies table if it does not exist
with engine.connect() as connection:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster_url TEXT NOT NULL
        )
    """))
    connection.commit()

def list_movies(get_all_data=False):
    """Retrieve all movies from the database.
    Default set to false, to only return title, year, and rating.
    True returns all columns"""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating, poster_url FROM movies"))
        movies = result.fetchall()

    movie_list = []
    if not get_all_data:
        for row in movies:
            movie_list.append({"title": row[0], "year": row[1], "rating": row[2]})
    else:
        for row in movies:
            movie_list.append({"title": row[0], "year": row[1], "rating": row[2], "poster_url": row[3]})
    return movie_list

def get_movies(get_all_data=False):
    """Same as list_movies(). Just for downward compatibility."""
    return list_movies(get_all_data)

def get_movie(title):
    """Retrieve a single movie by title from the database."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM movies WHERE title=:title"), {"title": title})
        movie = result.fetchone()
    return movie

def add_movie(title, year, rating, poster_url=""):
    """Add a new movie to the database."""
    with engine.begin() as connection:
        try:
            connection.execute(text("INSERT INTO movies (title, year, rating, poster_url) VALUES (:title, :year, :rating, :poster_url);"),
                               {"title": title, "year": year, "rating": rating, "poster_url": poster_url})
            print(f"Movie '{title}' added successfully.")
        except Exception as e:
            print(f"Error: {e}")

def delete_movie(title):
    """Delete a movie from the database."""
    if not title:
        return
    with engine.begin() as connection:
        try:
            connection.execute(text("DELETE FROM movies WHERE title=:title"), {"title": title})
            connection.commit()
            print(f"Movie '{title}' deleted successfully.")
        except Exception as e:
            print(f"Error: {e}")

def update_movie(title, rating):
    """Update a movie's rating in the database."""
    if not title or not rating:
        return
    with engine.connect() as connection:
        try:
            connection.execute(text("UPDATE movies SET rating=:rating WHERE title=:title"), {"title": title, "rating": rating})
            connection.commit()
            print(f"Movie '{title}' updated successfully.")
        except Exception as e:
            print(f"Error: {e}")
