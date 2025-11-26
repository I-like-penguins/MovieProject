#    "since we want you to choose how to implement it.
#    You can store the movie information inside the
#    JSON format however you want." -
#    so I won't output a dictionary of dictionairies and
#    choose my self-defined structure from before
#    of lists of dictionaries.
import json

# File will be data.json
FILE_NAME = "../data.json"


def get_movies():
    """
    The function loads the information from the JSON
    file and returns the data.

    The function returns:
    [
      { "title": "Titanic",
        "rating": 9.0,
        "year": 1999
      },
      "..." {
        ...
      },
    ]
    This is also the structure of the JSON file"""
    tmp_json = []
    with open(FILE_NAME, "r") as json_file:
        tmp_json = json.loads(json_file.read())
    return tmp_json


def save_movies(movies):
    """
    Gets all your movies as an argument and saves them to the JSON file.
    Does not fix ordering.
    """
    if not movies:
        print(f"There are no movies to save to file.")
        return
    try:
        with open(FILE_NAME, "w") as json_file:
            json_file.write(json.dumps(movies))
    except:
        print(f"Error saving file.")


def add_movie(title, year, rating):
    """
    Adds a movie to the movies database.
    Loads the information from the JSON file, add the movie,
    and saves it. The function doesn't need to validate the input.
    New movie will be ordered into JSON-entries
    """
    json_obj = []
    try:
        with open(FILE_NAME, "r") as json_read_file:
            json_read_file.seek(0)  # to make sure file read starts at beginning
            json_obj = json.loads(json_read_file.read())
    except:
        print(f"Error re-loading file. Skip file save.")
        return
    json_obj.append({"title": title, "rating": rating, "year": year})
    json_obj = sorted(json_obj, key=lambda movie: movie["rating"], reverse=True)
    try:
        with open(FILE_NAME, "w") as json_file:
            json_file.seek(0)
            json_file.write(json.dumps(json_obj))
    except:
        print(f"Error saving file.")


def delete_movie(title):
    """
    Deletes a movie from the movies database.
    Loads the information from the JSON file, deletes the movie,
    and saves it. The function doesn't need to validate the input.
    """
    json_obj = []
    try:
        with open(FILE_NAME, "r") as json_read_file:
            json_read_file.seek(0)
            json_obj = json.loads(json_read_file.read())
    except:
        print(f"Error re-loading file. Skip file save.")
        return
    index_to_delete = 0
    bln_no_title_found = True
    for movie in json_obj:
        if movie["title"].lower() == title.lower():
            bln_no_title_found = False
            break
        index_to_delete += 1
        if not bln_no_title_found:  # check to prevent false deletion of last entry
            del (json_obj[index_to_delete])
    try:
        with open(FILE_NAME, "w") as json_file:
            json_file.seek(0)
            json_file.write(json.dumps(json_obj))
    except:
        print(f"Error saving file.")


def update_movie(title, rating):
    """
    Updates a movie from the movies database.
    Loads the information from the JSON file, updates the movie,
    and saves it. The function doesn't need to validate the input.
    """
    try:
        with open(FILE_NAME, "r") as json_read_file:
            json_read_file.seek(0)
            json_obj = json.loads(json_read_file.read())
    except:
        print(f"Error re-loading file. Skip file save.")
        return
    for movie in json_obj:
        if movie["title"].lower() == title.lower():
            movie["rating"] = rating
    try:
        with open(FILE_NAME, "w") as json_file:
            json_file.seek(0)
            json_file.write(json.dumps(json_obj))
    except:
        print(f"Error saving file.")