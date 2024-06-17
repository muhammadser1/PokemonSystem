import json
import threading
import requests
from constants import pokemonApi_url, json_url


def correct_pokemon_data(pokemon, memo):
    """

    corrects the data of a single Pokemon by fetching its type information from the Pokemon API.
    """
    name = pokemon["name"]
    url = f"{pokemonApi_url}{name}"
    response = requests.get(url).json()
    tmp = []
    for type in response["types"]:
        tmp.append(type["type"]["name"])
    pokemon["type"] = tmp
    memo.append(pokemon)


def read_json():
    """
    Reads the JSON data from the specified file.

    :return: The data read from the JSON file.
    """

    with open(json_url, 'r') as file:
        data = json.load(file)
    return data


def write_to_json(data):
    """
    Writes the given data to the specified JSON file.

    :param data: The data to write to the JSON file.
    :return: None
    """
    with open(json_url, 'w') as file:
        json.dump(data, file)


def create_threads_for_updating_json():
    """
    Creates and starts threads to update the Pokémon data in the JSON file concurrently.

    :return: The updated Pokémon data.
    """
    json_db = read_json()
    memo = []
    threads = []
    for pokemon in json_db:
        thread = threading.Thread(target=correct_pokemon_data, args=(pokemon, memo))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

    write_to_json(json_db)
    return json_db


json_db = create_threads_for_updating_json()
