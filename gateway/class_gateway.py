import base64

from constant import *
import requests
from schema import *
from fastapi import HTTPException

class ClassGateway:
    def __init__(self):
        self.flag = 0

    def fetch_pokemon_by_id(self, pokemon_id: int):
        """
            Retrieve a Pokemon by its ID.
            :param pokemon_id: The ID of the Pokémon to retrieve
            :return: Pokémon data
        """
        url = f"{POKEMON_SERVER_URL}{pokemon_id}"
        response = requests.get(url)
        return response

    def get_image_of_pokemon(self, pokemon_name: str):
        url = f"{pokemoon_api_get_img}{pokemon_name}"
        response = requests.get(url)
        return response

    def get_pokemons_by_trainer(self, trainer_name):
        url = f"{POKEMON_SERVER_URL}?trainer_name={trainer_name}"
        pokemons = requests.get(url)
        return pokemons.json()

    def get_pokemons_by_type(self, type):
        url = f"{POKEMON_SERVER_URL}?pokemon_type={type}"
        pokemons = requests.get(url)
        return pokemons.json()

    def fetch_trainers_by_pokemon_name(self, pokemon_name):
        url = f"{Trainer_SERVER_URL}pokemons/{pokemon_name}"
        response = requests.get(url)
        return response.json()

    def decode_detail(self,respond):
        content = respond.content.decode("utf-8")
        detail = respond.json().get("detail", content)
        return detail
    # def fetch_trainer_by_trainerName(self, trainerName: str):
    #     url = f"{Trainer_SERVER_URL}{trainerName}"
    #     response = requests.get(url)
    #     return response.json()
    #
    # def fetch_trainers_by_pokemonName(self, pokemon_name: str):
    #     url = f"{Trainer_SERVER_URL}pokemons/{pokemon_name}"
    #     response = requests.get(url)
    #     return response.json()
    #
    # def check_existing_team(self, trainer_name: str, pokemon: str):
    #     trainers_with_pokemon = self.fetch_trainers_by_pokemonName(pokemon)
    #     is_trainer_in_team = any(trainer_name in trainer for trainer in trainers_with_pokemon)
    #     return is_trainer_in_team
    #
    def add_pokemon_to_trainer(self, trainer_name: str, pokemon_id: str):
        url = f"{Trainer_SERVER_URL}{trainer_name}/pokemons/{pokemon_id}"
        response = requests.post(url)
        return response

    def delete_pokemon_from_trainer(self, trainer_name: str, pokemon_id: str):
        url = f"{Trainer_SERVER_URL}{trainer_name}/pokemons/{pokemon_id}"
        response = requests.delete(url)
        return response

    def is_pokemon_name_in_db(self, pokemon_name: str):
        url = f"{POKEMON_SERVER_URL}name/{pokemon_name}"
        response = requests.get(url)
        return response.json()

    def fetch_pokemonApi_by_name(self, pokemon_name: str):
        url = f"{POKEMON_Api_URL}{pokemon_name}"
        response = requests.get(url)
        return response

    def add_pokemon(self, pokemon_data):
        url = f"{POKEMON_SERVER_URL}"
        pokemon = Pokemon(id=pokemon_data["pokemon_Data"][0], name=pokemon_data["pokemon_Data"][1],
                          height=pokemon_data["pokemon_Data"][2]
                          , weight=pokemon_data["pokemon_Data"][3], types=pokemon_data["types"])
        response = requests.post(url, json=pokemon.dict())
        return response

    def add_img(self,pokemon_name:str):
        url = f"{POKEMON_Api_URL}img/{pokemon_name}"
        response = requests.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch image")

        encoded_image = base64.b64encode(response.content).decode('utf-8')
        img={
            "name":pokemon_name,
            "bytes":encoded_image
        }
        url = f"{pokemon_api_img}"

        response_content = requests.post(url,json=img)
        return response_content