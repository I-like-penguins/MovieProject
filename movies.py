import random
import movie_storage


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
    print("4. Update movie")
    print("5. Stats")
    print("6. Random movie")
    print("7. Search movie")
    print("8. Movies sorted alphabetically")
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


def add_movie(movies_dict):
    """Function to add a new movie to the list of dictionaires.
    Ordering of the list has to be done externaly.
    Also calls add_movie-function of movie_storage to save to JSON-file."""
    # input for title-entry
    title = input(f"Please enter a movie title first: ")
    if not title:
        print(f"You did not enter a title. Back to menu.")
        return
    # input for rating-entry
    rating = 0.0
    try:
        print(f"Now, please give this movie a rating in floating point value.")
        rating = float(input(f"Value should be between 0.0 and 10.0:  "))
    except ValueError:
        print(f"You did not give this movie a rating. Movie will be given a standard rating of 5.0.")
        rating = 5.0
    if rating > 10.0:
        print(f"Wow, that movie must be great. But rating will be kept to 10.0")
        rating = 10.0
    if rating < 0.0:
        print(f"A movie can not be that bad, can it? We will keep it at 0.0.")
        rating = 0.0
    # input for year-entry
    try:
        year = int(input(f"Now, please give this movie a year of release: "))
        if year < 1888:
            print(
                f"The first movie ever made was Roundhay Garden Scene from 1888. So release-year will be kept at 1888.")
            year = 1888
    except ValueError:
        print(f"You did not give this movie a release-year. Movie will be given a standard year of 2000.")
        year = 2000

    movies_dict.append({"title": title, "rating": rating, "year": year})
    movie_storage.add_movie(title, year, rating)


def delete_movie(movies_dict):
    """Deletes an entry in the list of movies.
    Handles the user-input.
    Also deletes the same entry in the JSON file"""
    list_all_movies(movies_dict)
    print(f"Which movie do you want to delete? Please look at the list above.")

    try:
        index_to_delete = int(input(f"Please enter a number now: "))
        if index_to_delete < 1 or index_to_delete > len(movies_dict):
            print(f"There is no film title in this place.")
            return
        try:
            print(f"{movies_dict[index_to_delete - 1]["title"]} will be deleted!")
            movie_storage.delete_movie(movies_dict[index_to_delete - 1]["title"])
        except:
            print(f"Error handling file input/output")
        del (movies_dict[index_to_delete - 1])
        print(f"Movie deleted")
    except ValueError:
        print(f"You did not enter a number. Please come back when you are sure what to delete.")
    return


def update_movie(movies_dict):
    """Changes a rating of a user-specified title.
    Title has to be already known."""
    usr_input = input(f"Please enter a movie title: ")
    title_list = []
    for movie in movies_dict:
        title_list.append(movie["title"])
    if usr_input in title_list:
        try:
            new_rating = float(input("Please enter new rating: "))
            movies_dict[title_list.index(usr_input)]["rating"] = new_rating
            movie_storage.update_movie(usr_input, new_rating)
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
    print(f"{movie["title"]}: {movie["rating"]}")


def search_movie(movies_dict):
    """Searches list for part of the movie title and
    prints all matches with corresponding ratings"""
    search_string = input(f"Enter part of movie name: ")
    for movie in movies_dict:
        if search_string.lower() in movie["title"].lower():
            print(f'{movie["title"]}, {movie["rating"]}')


# since movies are already sorted by rating this function prints alphabetically
def print_alphabetical(movies_dict):
    """Prints all movies in alphabetical order."""
    alphabetical_list = list(sorted(movies_dict, key=lambda movie: movie["title"], reverse=False))
    print(f"Here are all movies in alphabetical order:")
    for movie in alphabetical_list:
        print(f"{movie["title"]}: {movie["rating"]}")


def main():
    """Starts with initializing a JSON-file with basic values
    or reads existing JSON-file to fill the list with movies.
    Prints the basic menue and directs the user to
    corresponding functions which handle each menu point"""
    # initialize movies DB
    try:
        movies = movie_storage.get_movies()
    except FileNotFoundError:
        # Default list to store the movies as dictionaries
        # To reset just delete JSON-file
        movies = [
            {"title": "The Shawshank Redemption", "rating": 9.5, "year": 2000},
            {"title": "Pulp Fiction", "rating": 8.8, "year": 2000},
            {"title": "The Room", "rating": 3.6, "year": 2000},
            {"title": "The Godfather", "rating": 9.2, "year": 2000},
            {"title": "The Godfather: Part II", "rating": 9.0, "year": 2000},
            {"title": "The Dark Knight", "rating": 9.0, "year": 2000},
            {"title": "12 Angry Men", "rating": 8.9, "year": 2000},
            {"title": "Everything Everywhere All At Once", "rating": 8.9, "year": 2000},
            {"title": "Forrest Gump", "rating": 8.8, "year": 2000},
            {"title": "Star Wars: Episode V", "rating": 8.7, "year": 2000}
        ]
    movies = order_movies_database(movies)
    try:
        movie_storage.save_movies(movies)  # create file and/or save ordered list if file was tinkered externaly
    except:
        print(f"Unable to save file.")

    bln_exit = False
    while not bln_exit:
        print_menu()
        menu_choice = 0
        try:
            menu_choice = int(input(f"Enter choice (0-10): "))
        except ValueError:
            print(f"Please enter a number between 0 and 10 (inclusive).")
            continue
        if menu_choice == 1:
            list_all_movies(movies)
        elif menu_choice == 2:
            add_movie(movies)
            movies = order_movies_database(movies)
        elif menu_choice == 3:
            delete_movie(movies)
        elif menu_choice == 4:
            update_movie(movies)
            movies = order_movies_database(movies)
        elif menu_choice == 5:
            movie_stats(movies)
        elif menu_choice == 6:
            random_movie(movies)
        elif menu_choice == 7:
            search_movie(movies)
        elif menu_choice == 8:
            print_alphabetical(movies)
        elif menu_choice == 0:
            bln_exit = True
            print(f"Bye!")
        else:
            print(f"You've chosen a number outside your range of choice (1-9).")


if __name__ == "__main__":
    main()
