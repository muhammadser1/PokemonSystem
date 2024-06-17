from typing import Optional, List
import requests
from fastapi import APIRouter, Depends, Query, HTTPException
from models.mysql_database import get_db
from models.schema import Pokemon

router = APIRouter(prefix='/pokemons', tags=['All requests for Pokemon resources'])


@router.get("/{pokemon_id}")
def get_pokemon_by_id(pokemon_id: int, pokemon_db=Depends(get_db)):
    """
    retrieve a pokemon by its id
    :param pokemon_id: the id of pokemon to retrieve
    :param pokemon_db: Dependency to fetch the database.
    :return: pokemon data
    """
    pokemon_info = pokemon_db.get_pokemon_by_id(pokemon_id)
    if not pokemon_info:
        raise HTTPException(status_code=404, detail="No Pokemon found with the given ID")

    types = pokemon_db.get_type_of_pokemon(pokemon_id)
    pokemon = {"pokemon_info": pokemon_info, "types": types}
    return pokemon

#
# @router.get("/name/{pokemon_name}")
# def get_pokemon_by_name(pokemon_name: str, pokemon_db=Depends(get_db)):
#     """
#     retrieve a pokemon by its name
#     :param pokemon_id: the id of pokemon to retrieve
#     :param pokemon_name: Dependency to fetch the database.
#     :return: pokemon data
#     """
#     pokemon = pokemon_db.get_pokemon_by_name(pokemon_name)
#     if not pokemon:
#         raise HTTPException(status_code=404, detail="No Pokemon found with the given Name")
#     return pokemon[0]


@router.get("/")
def get_pokemon_with_filtering(trainer_name: Optional[str] = Query(None), pokemon_type: Optional[str] = Query(None),
                               pokemon_db=Depends(get_db)):
    """
    retreive pokemon with optinal filetering by trainer_name or pokemon type
    :param pokemon_name: retrieve a pokemon by its name
    :param trainer_name: the name of trainer to filter by
    :param pokemon_type: the type of pokemon to filter by
    :param pokemon_db: Dependency to fetch the database.
    :return:
    """

    if trainer_name:
        pokemons = pokemon_db.get_pokemon_by_trainer(trainer_name)
        if not pokemons:
            raise HTTPException(status_code=404, detail="No Pokemon found with the given trainer name")
        return pokemons

    if pokemon_type:
        pokemons = pokemon_db.get_pokemon_by_type(pokemon_type)
        if not pokemons:
            raise HTTPException(status_code=404, detail="No Pokemon found with the given type")
        return pokemons


@router.post("/")
def add_pokemon(pokemon: Pokemon, pokemon_db=Depends(get_db)):

    pokemon_name = pokemon_db.get_pokemon_by_name(pokemon.name)
    if pokemon_name:
        raise HTTPException(status_code=409, detail="Pokemon found in DB")

    pokemon_info = [pokemon.id, pokemon.name, pokemon.height, pokemon.weight]
    pokemon_types = pokemon.types
    pokemon_db.add_pokemon(pokemon_info)
    pokemon_db.add_pokemonsTypes(pokemon.id, pokemon_types)
    return {"message": "Pokemon added successfully."}
