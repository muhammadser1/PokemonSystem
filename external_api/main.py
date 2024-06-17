import base64
import requests
from fastapi import FastAPI, HTTPException
from utils.pokemon_data import get_pokemon_from_api, extract_pokemon_data, extract_pokemon_types, \
    fetch_image_from_pokemonApi
from fastapi.responses import StreamingResponse
import io

server = FastAPI()


@server.get("/pokemons/{pokemon_name}")
def fetch_pokemon_from_api(pokemon_name: str):
    pokemon = get_pokemon_from_api(pokemon_name)
    if not pokemon:
        raise HTTPException(status_code=404, detail="No Pokemon found in pokemonApi")

    pokemon_data = extract_pokemon_data(pokemon)
    types = extract_pokemon_types(pokemon)
    pokemon = {"pokemon_Data": pokemon_data, "types": types}
    return pokemon


@server.get("/pokemons/img/{pokemon_name}")
def fetch_imgPokemon_from_api(pokemon_name: str):
    pokemon = get_pokemon_from_api(pokemon_name)
    if not pokemon:
        raise HTTPException(status_code=404, detail="No Pokemon found in pokemonApi")
    response_img = fetch_image_from_pokemonApi(pokemon)
    return StreamingResponse(io.BytesIO(response_img), media_type="image/png")
