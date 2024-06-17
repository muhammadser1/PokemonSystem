from db_connection import connect_to_database_mysql
from json_handler import read_json
import mysql.connector
from mysql.connector import Error


def insert_data(cursor, sql_query, data):
    """Execute an SQL insert statement with the provided data."""
    try:
        cursor.execute(sql_query, data)
    except Error as err:
        print(f"Error: {err}")


def insert_pokemons(cursor, data):
    """Insert Pokemon data into the pokemons table."""
    sql_insert_query = """
    INSERT INTO pokemons (id, name, height, weight)
    VALUES (%s, %s, %s, %s);
    """
    for pokemon in data:
        pokemon_data = (pokemon["id"], pokemon["name"], pokemon["height"], pokemon["weight"])
        insert_data(cursor, sql_insert_query, pokemon_data)


def insert_types(cursor, data):
    """Insert unique types into the types table."""
    types = set()
    sql_insert_query = """
    INSERT INTO types (name)
    VALUES (%s);
    """
    for pokemon in data:
        for t in pokemon["type"]:
            if t not in types:
                types.add(t)
                insert_data(cursor, sql_insert_query, (t,))


def insert_trainers(cursor, data):
    """Insert unique trainers into the trainers table."""
    trainers = set()
    sql_insert_query = """
    INSERT INTO trainers (name, town)
    VALUES (%s, %s);
    """
    for pokemon in data:
        for owner in pokemon["ownedBy"]:
            if owner["name"] not in trainers:
                trainers.add(owner["name"])
                insert_data(cursor, sql_insert_query, (owner["name"], owner["town"]))


def insert_pokemon_types(cursor, data):
    """Insert Pokemon-type relationships into the pokemon_types table."""
    sql_insert_query = """
    INSERT INTO pokemon_types (type_name, pokemon_id)
    VALUES (%s, %s);
    """
    for pokemon in data:
        for type_ in pokemon["type"]:
            insert_data(cursor, sql_insert_query, (type_, pokemon["id"]))


def insert_teams(cursor, data):
    """Insert trainer-Pokemon relationships into the teams table."""

    sql_select_trainers = "SELECT name FROM trainers"
    cursor.execute(sql_select_trainers)
    trainers_in_db = cursor.fetchall()
    trainer_names = {row[0] for row in trainers_in_db}

    sql_insert_query = """
    INSERT INTO teams (trainer_name, pokemon_id)
    VALUES (%s, %s);
    """
    for pokemon in data:
        for trainer in pokemon["ownedBy"]:
            if trainer["name"] in trainer_names:
                insert_data(cursor, sql_insert_query, (trainer["name"], pokemon["id"]))


