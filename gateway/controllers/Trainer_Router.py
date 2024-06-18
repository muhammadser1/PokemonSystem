import requests
from fastapi import APIRouter, Query, HTTPException
from class_gateway import ClassGateway

router = APIRouter(prefix='/trainers', tags=['Trainers'])
gateway_instance = ClassGateway()


@router.get("/pokemon/{pokemon_name}")
def get_trainers_by_pokemon_name(pokemon_name: str):
    """
    Retrieves a list of trainers who own a Pokemon with the given name.

    :param pokemon_name: The name of the Pokemon to search for.
    :return: A list of trainers who own the Pokemon.
    """
    trainers = gateway_instance.fetch_trainers_by_pokemon_name(pokemon_name)
    if not trainers:
        raise HTTPException(status_code=404, detail=f"No trainers found for Pokemon with name '{pokemon_name}'")

    return trainers


@router.post("/{trainer_name}/pokemons/{pokemon_id}")
def add_pokemon_to_trainer(trainer_name: str, pokemon_id: int):
    """
    Add a Pokémon to a trainer's team.

    :param trainer_name: The name of the trainer.
    :param pokemon_id: The ID of the Pokémon to add.
    :return: Success message or error message.
    """

    respond=gateway_instance.add_pokemon_to_trainer(trainer_name, pokemon_id)
    if respond.status_code!=200:
        detail=gateway_instance.decode_detail(respond)
        raise HTTPException(status_code=respond.status_code,detail=detail)

    return {"msg": "Pokemon added to the trainer's team successfully"}


@router.delete("/{trainer_name}/pokemons/{pokemon_id}")
def delete_pokemon_from_trainer_team(trainer_name: str, pokemon_id: int):

    respond=gateway_instance.delete_pokemon_from_trainer(trainer_name, pokemon_id)
    if respond.status_code!=200:
        detail=gateway_instance.decode_detail(respond)
        raise HTTPException(status_code=respond.status_code,detail=detail)


    return {"detail": "Pokemon removed from the trainer's team successfully"}
