import requests
from requests import Response
import json
import os
from dotenv import load_dotenv

class data_fetcher:
    """ Fetches the animal's data from a JSON file or an API endpoint.
    Returns a list of animals, each animal is a representation of a dictionary."""
    def __init__(self):
        load_dotenv()
        self.__API_KEY = os.getenv('API_KEY')

    def __load_api_data(self, url) -> Response:
        """ Loads data from an API endpoint and returns response-object"""
        response = requests.get(url)
        return response

    def __load_data(self, file_path: str):
       """ Loads a JSON file """
       with open(file_path, "r") as handle:
           return json.load(handle)

    def return_data(self, usr_input: str, is_json: bool = True):
        """ Returns data from a JSON file or a specific API endpoint """
        if is_json:
            return self.__load_data(usr_input)
        else:
            try:
                return self.__load_api_data(f"http://www.omdbapi.com/?apikey={self.__API_KEY}&t={usr_input}").json()
            except:
                print(f"Error fetching data from API")
                return None
