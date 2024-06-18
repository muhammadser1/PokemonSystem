import base64
from typing import Dict, Any, Optional
import requests
from fastapi import APIRouter, Query, HTTPException
from class_gateway import ClassGateway
from fastapi.responses import StreamingResponse
import io

router = APIRouter(prefix='/pokemons', tags=['Pokemons'])
gateway_instance = ClassGateway()


@router.get("/{pokemon_id}")
def get_pokemon_by_id(pokemon_id: int):
    """
    Retrieve a Pokemon by its ID.

    :param pokemon_id: The ID of the Pokémon to retrieve
    :return: Pokémon data including image in Base64 format
    """
    pokemon = gateway_instance.fetch_pokemon_by_id(pokemon_id)
    if pokemon.status_code==404:
        raise HTTPException(status_code=404, detail="No Pokemon found with the given ID")
    pokemon=pokemon.json()
    pokemon_name = pokemon["pokemon_info"][0][1]

    img_bytes_response = gateway_instance.get_image_of_pokemon(pokemon_name)
    if img_bytes_response.status_code==404:
        raise HTTPException(status_code=404, detail="No image found for the given Pokemon")

    img_bytes=img_bytes_response.content
    if img_bytes:
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    else:
        img_base64 = None

    data_json = {"pokemon": pokemon,"img_base64": img_base64}
    return data_json


@router.get("/")
def get_pokemon_with_filtering(trainer_name: Optional[str] = Query(None), pokemon_type: Optional[str] = Query(None)):
    if trainer_name:
        pokemons= gateway_instance.get_pokemons_by_trainer(trainer_name)
        if not pokemons:
            raise HTTPException(status_code=404, detail="No Pokemon found with the given trainer_name")
        return pokemons

    if pokemon_type:
        pokemons = gateway_instance.get_pokemons_by_type(pokemon_type)
        if not pokemons:
            raise HTTPException(status_code=404, detail="No Pokemon found with the given type")
        return pokemons


@router.post("/")
def create_pokemon(pokemon_name: str):
    """
    Create a new Pokemon.
    """

    pokemon_data_respond=gateway_instance.fetch_pokemonApi_by_name(pokemon_name)
    if pokemon_data_respond.status_code!=200:
        detail=gateway_instance.decode_detail(pokemon_data_respond)
        raise HTTPException(status_code=pokemon_data_respond.status_code,detail=detail)
    pokemon_data=pokemon_data_respond.json()

    response_add_data=gateway_instance.add_pokemon(pokemon_data)
    if response_add_data.status_code!=200:
        detail=gateway_instance.decode_detail(response_add_data)
        raise HTTPException(status_code=response_add_data.status_code,detail=detail)
    response_add_img=gateway_instance.add_img(pokemon_name)
    if response_add_img.status_code!=200:
        detail=gateway_instance.decode_detail(response_add_img)
        raise HTTPException(status_code=response_add_img.status_code,detail=detail)
    return {"msg": "Pokemon created "}
