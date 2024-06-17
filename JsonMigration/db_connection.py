import mysql.connector
from mysql.connector import Error
from sqlConfig import MYSQL_USER, MYSQL_DATABASE, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT
# import pymongo
# from gridfs import GridFS


def connect_to_database_mysql():
    """Connect to the MySQL database and return the connection object."""
    try:
        db = mysql.connector.connect(
            host="localhost",
            user=f"{MYSQL_USER}",
            password=f"{MYSQL_PASSWORD}",
            database=f"{MYSQL_DATABASE}",
            port=MYSQL_PORT
        )
        return db
    except Error as err:
        print(f"Error: {err}")
        return None


# def connect_to_database_mongodb():
#     url_mongo = "mongodb://mongodb:27017/"
#     mongo = pymongo.MongoClient(url_mongo)
#     db = mongo["pokemons"]
#     fs = GridFS(db)
#     return fs,db
