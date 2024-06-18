import requests
from fastapi import APIRouter, Query, HTTPException,Request
from class_gateway import ClassGateway
from redis_class import get_redis

router = APIRouter(prefix='/trainers', tags=['Trainers'])
gateway_instance = ClassGateway()
redis_client = get_redis()


@router.get("/pokemon/{pokemon_name}")
def get_trainers_by_pokemon_name(request: Request,pokemon_name: str):
    # full_path = request.url.path
    """
    Retrieves a list of trainers who own a Pokemon with the given name.

    :param pokemon_name: The name of the Pokemon to search for.
    :return: A list of trainers who own the Pokemon.
    """
    trainers = gateway_instance.fetch_trainers_by_pokemon_name(pokemon_name)
    if not trainers:
        raise HTTPException(status_code=404, detail=f"No trainers found for Pokemon with name '{pokemon_name}'")

    # redis_client.set_(full_path, trainers, 10)
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
