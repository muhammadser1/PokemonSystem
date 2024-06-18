import requests
import mysql.connector
from models.database import Database
from sqlConfig import MYSQL_USER,MYSQL_DATABASE,MYSQL_PASSWORD,MYSQL_HOST,MYSQL_PORT

def get_db():
    db = Mysql_database()
    return db


class Mysql_database(Database):
    def __init__(self):
        self.config = {
            'user': f"{MYSQL_USER}",
            'password': f"{MYSQL_PASSWORD}",
            'host': f"{MYSQL_HOST}",
            'port': MYSQL_PORT,
            'database': f"{MYSQL_DATABASE}"
        }
        self.connetion = self.connect()

    def connect(self):
        mydb = mysql.connector.connect(**self.config)
        return mydb

    def __execute_query(self, query, commit=False):
        mydb = self.connect()
        cursor = mydb.cursor()
        cursor.execute(query)
        if commit:
            mydb.commit()
        return cursor.fetchall()

    ####################################################################################################################
    """ Getters for Pokemons """

    def get_pokemon_by_id(self, id: int):
        query = f"""SELECT * FROM pokemons WHERE id = '{id}'"""
        return self.__execute_query(query)

    def get_pokemon_by_name(self, name: str):
        query = f"""SELECT * FROM pokemons WHERE name = '{name}'"""
        return self.__execute_query(query)

    def get_pokemon_by_type(self, type: str):
        query = f"SELECT p.name FROM pokemons p join pokemon_types pt on  p.id = pt.pokemon_id where pt.type_name = '{type}'"
        pokemons = self.__execute_query(query)
        pokemons = [list(inner_list) for inner_list in pokemons]
        return pokemons

    def get_type_of_pokemon(self,id:int):
        query=f"select type_name from pokemon_types where pokemon_id={id}"
        types = self.__execute_query(query)
        return types

    def get_pokemon_by_trainer(self, trainer: str):
        query = f"""SELECT p.name FROM pokemons p JOIN teams ON p.id = teams.pokemon_id JOIN trainers t ON t.name = teams.trainer_name WHERE t.name = '{trainer}';"""
        pokemons = self.__execute_query(query)
        pokemons = [list(inner_list) for inner_list in pokemons]
        return pokemons

    ####################################################################################################################
    """ Getters for Trainers """

    def get_trainer_by_name(self, name: str):
        query = f"""SELECT * FROM trainers WHERE name = '{name}'"""
        return self.__execute_query(query)

    def get_trainers_by_pokemon_name(self, pokemon: str):
        query = f"SELECT t.name FROM trainers t join teams on  t.name = teams.trainer_name join pokemons p on p.id = teams.pokemon_id  where p.name = '{pokemon}'"
        trainers=self.__execute_query(query)
        trainers = [list(inner_list) for inner_list in trainers]
        return trainers

    ####################################################################################################################
    """ Operations"""

    def add_pokemon_to_trainer(self, trainer_name, pokemon_id):
        query = f"INSERT INTO teams (trainer_name, pokemon_id) VALUES ('{trainer_name}',{pokemon_id});"
        return self.__execute_query(query, True)

    def add_pokemon(self, pokemon):
        query = f"INSERT INTO pokemons (id, name, height, weight) VALUES ({pokemon[0]},'{pokemon[1]}', {pokemon[2]}, {pokemon[3]});"
        self.__execute_query(query, commit=True)

    def delete_pokemon_from_trainer_Team(self, trainer_name,pokemon_id):
        query = f"DELETE from teams where trainer_name='{trainer_name}' and pokemon_id={pokemon_id};"
        return self.__execute_query(query, True)

    def add_pokemonsTypes(self, pokemon_id: int, types: list):
        for type in types:
            query = f"""INSERT INTO pokemon_types (type_name, pokemon_id) VALUES ('{type}', {pokemon_id});"""
            self.__execute_query(query, commit=True)
    ####################################################################################################################
    def get_team_by_trainer_pokemon(self,trainer_name,pokemon_id):
        query=f"select * from teams where teams.trainer_name='{trainer_name}' and teams.pokemon_id={pokemon_id};"
        print(query)
        return self.__execute_query(query)