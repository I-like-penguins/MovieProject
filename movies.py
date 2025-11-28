import random
#import movie_storage
import movie_storage.movie_storage_sql
import data_fetcher as df
import os
from dotenv import load_dotenv

from web_generator import load_template, serialize_movie, write_html


def print_menu():
    """Prints a basic menu. Does nothing else.
    User-input has to be handled externaly"""
    print("********** My Movies Database **********")
    print("")
    print("Menu:")
    print("0. Exit programm")
    print("1. List movies")
    print("2. Add movie")
    print("3. Delete movie")
    print("4. Stats")
    print("5. Random movie")
    print("6. Search movie")
    print("7. Movies sorted alphabetically")
    print("8. Generate website")
    print("")


# order movies-dictionary by rating (value) in descending order
def order_movies_database(movies_dict, reversal=True) -> list:
    """Orders a list of dictionaries of movies based on their raiting."""
    return list(sorted(movies_dict, key=lambda movie: movie["rating"], reverse=reversal))


def print_all_values(movie, counter_value=(-1)):
    """Prints all values of a single movie (dict).
    Basic idea is to print every possible value, like title,
    rating and whatever else: Can be re-used indeffenetly/is
    value-independent.
    optionally: Also print a numbering for an ordered list:
    counting has to be done outside this function.
    -1 or below: No numbering."""
    if not movie:
        print(f"Error: There was no movie to print.")
        return
    if counter_value > (-1):  # optional numbering
        print(f"{counter_value}. ", end="")
    i = 1  # check for last entry in print per movie
    for k, v in movie.items():
        if i < len(movie.items()):
            print(f'{k}: {v} - ', end="")
            i += 1
        else:  # print last element in dictionary
            print(f'{k}: {v}', end="")
    print("")  # newline

def list_all_movies(movies_dict):
    """Prints all list-entries if there are any.
    Uses print_all_values(...) for each individual entry,
    with counting."""
    if not movies_dict:
        print(f"There are no movies in the list.")
        return
    counter = 1
    for movie in movies_dict:
        print_all_values(movie, counter)
        counter += 1

    print(f"Total number of movies: {counter - 1}")
    input(f"Please press enter to continue.")
    return

def list_all_movies_sql():
    """Prints all list-entries if there are any.
    Uses print_all_values(...) for each individual entry,
    with counting."""
    movies = movie_storage.movie_storage_sql.get_movies()
    if not movies:
        print(f"There are no movies in the list.")
        return []
    counter = 1
    for movie in movies:
        print_all_values(movie, counter)
        counter += 1
    return movies

def add_movie(movies_dict):
    """Function to add a new movie to the list of dictionaires from ombd api. Safes the
    results to movie_storage"""
    # input for title-entry
    title = input(f"Please enter a movie title first: ")
    if not title:
        print(f"You did not enter a title. Back to menu.")
        return
    else:
        title = title.strip()
        api_data = df.data_fetcher()
        try:
            tmp_movie_json = api_data.return_data(title, False)
            if tmp_movie_json["imdbRating"] == "N/A":
                tmp_movie_json["imdbRating"] = 0.0
            movie_storage.movie_storage_sql.add_movie(tmp_movie_json["Title"], int(tmp_movie_json["Year"]), float(tmp_movie_json["imdbRating"]), tmp_movie_json["Poster"])
        except KeyError as ke:
            if tmp_movie_json["Response"].lower() == "false":
                print(f"There is no movie with this title. Back to menu.")
        except TypeError as te:
            print(f"Error: {te}. Back to menu.")

def delete_movie():
    """Deletes an entry in the list of movies.
    Handles the user-input.
    Also deletes the same entry in the JSON file"""
    movies = list_all_movies_sql()
    print(f"Which movie do you want to delete? Please look at the list above.")
    if len(movies) == 0:
        print(f"There are no movies in the list.")
        return
    try:
        index_to_delete = int(input(f"Please enter a number now: "))
        if index_to_delete < 1 or index_to_delete > len(movies):
            print(f"There is no film title in this place.")
            return
        try:
            print(f"{movies[index_to_delete - 1]['title']} will be deleted!")
            movie_storage.movie_storage_sql.delete_movie(movies[index_to_delete - 1]['title'])
        except Exception as e:
            print(f"Error handling file input/output: {e}")
        print(f"Movie deleted")
    except ValueError:
        print(f"You did not enter a number. Please come back when you are sure what to delete.")
    return

def update_movie(movies_dict):
    """Deprecated"""
    usr_input = input(f"Please enter a movie title: ")
    title_list = []
    for movie in movies_dict:
        title_list.append(movie["title"])
    if usr_input in title_list:
        try:
            new_rating = float(input("Please enter new rating: "))
            movies_dict[title_list.index(usr_input)]["rating"] = new_rating
        except ValueError:
            print(f"Invalid rating. Must be floating point.")
    else:
        print(f"Movie does not exist.")


# prints statistics about the movie database
def movie_stats(movies_dict):
    """Takes the list of movies and prints some statistics:
    Average and median rating.
    Best and Worst movie(s).
    Lists all best/worst movies if there are multiple entries
    with the same best/worst rating
    Uses print_all_values(...) without a counter to print
    every movie-related value."""
    reordered_db = order_movies_database(movies_dict, False)  # Median needs ascending order

    # initialize block
    list_of_ratings = []
    lowest = 10.0
    highest = 0.0
    lowest_rated_movies = []
    highest_rated_movies = []
    median = 0.0
    sum = 0.0

    for movie in reordered_db:
        if movie["rating"] < lowest:  # clear list of lowest rated movies and start a new
            lowest = movie["rating"]
            lowest_rated_movies = []
            lowest_rated_movies.append(movie)
        elif movie["rating"] == lowest:  # add to existing lowest rated list
            lowest_rated_movies.append(movie)
        if movie["rating"] > highest:  # clear list of highest rated movies and start a new
            highest = movie["rating"]
            highest_rated_movies = []
            highest_rated_movies.append(movie)
        elif movie["rating"] == highest:  # add to existing highest rated list
            highest_rated_movies.append(movie)
        list_of_ratings.append(movie["rating"])
        sum += movie["rating"]

    # calculate median and average
    list_length = len(list_of_ratings)

    average = sum / list_length
    if list_length % 2 == 0:
        median = 0.5 * (list_of_ratings[int(list_length / 2)] + list_of_ratings[int(list_length / 2) - 1])
    else:
        median = list_of_ratings[int(list_length / 2)]

    print(f"Average rating: {average}")
    print(f"Median rating: {median}")
    print(f"-- The worst movie(s) --")
    for movie in lowest_rated_movies:
        print_all_values(movie)
    print(f"-- The best movie(s) --")
    for movie in highest_rated_movies:
        print_all_values(movie)
    print("")


def random_movie(movies_dict):
    """Prints a random movie out of the list of all movies"""
    rand_number = random.randint(0, len(movies_dict) - 1)
    movie = movies_dict[rand_number]
    print(f"{movie['title']}: {movie['rating']}")


def search_movie(movies_dict):
    """Searches list for part of the movie title and
    prints all matches with corresponding ratings"""
    search_string = input(f"Enter part of movie name: ")
    bln_found = False
    for movie in movies_dict:
        if search_string.lower() in movie["title"].lower():
            print(f'{movie["title"]}, {movie["rating"]}')
            bln_found = True
    if not bln_found:
        print(f"No movie found.")


# since movies are already sorted by rating this function prints alphabetically
def print_alphabetical(movies_dict):
    """Prints all movies in alphabetical order."""
    alphabetical_list = list(sorted(movies_dict, key=lambda movie: movie["title"], reverse=False))
    print(f"Here are all movies in alphabetical order:")
    for movie in alphabetical_list:
        print(f"{movie['title']}: {movie['rating']}")


def generate_website(movies):
    """Generates a website with all movies, their ratings, year and poster. Needs a html-template."""
    load_dotenv()
    try:
        template = load_template(os.getenv("TEMPLATE_PATH"))
        template = template.replace("__TEMPLATE_TITLE__", os.getenv("TEMPLATE_TITLE"))
        output_string = f""
        for movie in movies:
            print(f"Adding movie {movie['title']} to website.")
            output_string += serialize_movie(movie)
        write_html(os.getenv("OUTPUT_PATH"), template.replace("__TEMPLATE_MOVIE_GRID__", output_string))
        print("Website generated successfully.")
    except FileNotFoundError as e:
        print("Error handling file input/output.")

def main():
    """Prints the basic menue and directs the user to
    corresponding functions which handle each menu point"""
    # initialize movies DB
    movies = movie_storage.movie_storage_sql.get_movies()
    if not movies:
        movies = []
    #try:
    #    movie_storage.save_movies(movies)  # create file and/or save ordered list if file was tinkered externaly
    #except:
    #    print(f"Unable to save file.")

    bln_exit = False
    while not bln_exit:
        print_menu()
        try:
            menu_choice = int(input(f"Enter choice (0-8): "))
        except ValueError:
            print(f"Please enter a number between 0 and 10 (inclusive).")
            continue
        if menu_choice == 1:
            list_all_movies_sql()
        elif menu_choice == 2:
            add_movie(movies)
        elif menu_choice == 3:
            delete_movie()
        elif menu_choice == 4:
            movie_stats(movie_storage.movie_storage_sql.get_movies())
        elif menu_choice == 5:
            random_movie(movie_storage.movie_storage_sql.get_movies())
        elif menu_choice == 6:
            search_movie(movie_storage.movie_storage_sql.get_movies())
        elif menu_choice == 7:
            print_alphabetical(movie_storage.movie_storage_sql.get_movies())
        elif menu_choice == 8:
            generate_website(movie_storage.movie_storage_sql.get_movies(True))
        elif menu_choice == 0:
            bln_exit = True
            print(f"Bye!")
        else:
            print(f"You've chosen a number outside your range of choice (1-9).")


if __name__ == "__main__":
    main()
