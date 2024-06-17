from fastapi import APIRouter, Depends
from models.mysql_database import get_db

router = APIRouter(prefix='/trainers', tags=['This is all  requests for trainers resources '])


@router.get("/{trainer_name}")
def get_trainer_by_name(trainer_name: str, pokemon_db=Depends(get_db)):
    trainers = pokemon_db.get_trainer_by_name(trainer_name)
    return trainers


@router.get("/pokemons/{pokemon_name}")
def get_trainer_by_pokemon_name(pokemon_name: str, pokemon_db=Depends(get_db)):
    """
    Retrieves a list of trainers who own a Pokemon with the given name.
    :param pokemon_name: the name of the pokemon to search for.
    :param pokemon_db: Dependency to fetch the db
    :return: A list of trainers who own pokemon
    """
    trainers = pokemon_db.get_trainers_by_pokemon_name(pokemon_name)
    return trainers


@router.post("/{trainer_name}/pokemons/{pokemon_id}")
def add_pokemon_to_trainer(trainer_name: str, pokemon_id: int, pokemon_db=Depends(get_db)):
    """

    :param trainer_name: the name of trainer who will own the pokemon
    :param pokemon_id: the Id of pokemon to be added
    :param pokemon_db: Dependency to fetch the db
    :return: None
    """

    pokemon_db.add_pokemon_to_trainer(trainer_name, pokemon_id)


@router.delete("/{trainer_name}/pokemons/{pokemon_id}")
def delete_pokemon_from_trainer_team(trainer_name: str, pokemon_id: int, pokemon_db=Depends(get_db)):
    """
    delete a Pokemon from a trainer's team.
    :param trainer_name: The name of the trainer.
    :param pokemon_id: The ID of the Pokémon to remove from the trainer's team.
    :param pokemon_db: Dependency to access the database.
    """
    pokemon_db.delete_pokemon_from_trainer_Team(trainer_name, pokemon_id)
