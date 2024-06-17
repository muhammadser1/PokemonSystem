from constants import pokemonImg
import requests


def fetch_img_from_api(pokemon_id:int):
    url = f"{pokemonImg}{pokemon_id}.png"
    img = requests.get(url)
    img_bytes = img.content
    return img_bytes
