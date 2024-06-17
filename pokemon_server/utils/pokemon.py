import requests

from constants import pokemonApi_url


def fetch_pokemon_from_api(pokemon_name: str):
    """
    Fetch Pokemon data from the external API.
    :param pokemon_name: The name of the Pokemon to fetch.
    :return: Pokemon data from the API.
    """
    url = f"{pokemonApi_url}/{pokemon_name}"
    response = requests.get(url)

    if response.status_code != 200:
        return []

    return response.json()


def extract_pokemon_types(pokemon_data):
    """
    Extract types from the Pokemon data.
    :param pokemon_data: The data of the Pokemon.
    :return: List of type names.
    """
    return [type_info["type"]["name"] for type_info in pokemon_data["types"]]


def extract_pokemon_data(pokemon_data):
    """
    Extract relevant Pokemon data.
    :param pokemon_data: The data of the Pokemon.
    :return: List containing the Pokemon's ID, name, height, and weight.
    """
    return [pokemon_data["id"], pokemon_data["name"], pokemon_data["height"], pokemon_data["weight"]]