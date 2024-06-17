import pymongo
from gridfs import GridFS
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import StreamingResponse
import requests
import io
from mongoConfig import MONGO_SERVICE


def get_db():
    db = Mongo_database()
    return db


class Mongo_database():
    def __init__(self):
        self.config = f"mongodb://{MONGO_SERVICE}:27017/"
        self.client = self.connect()
        self.db = self.client["pokemons"]
        self.collection = self.db["images"]
        self.fs = GridFS(self.db)

    def connect(self):
        mongo = pymongo.MongoClient(self.config)
        return mongo

    # def add_data(self, name: str, address: str):
    #     document_to_insert = {"name": name, "address": address}
    #     result = self.collection.insert_one(document_to_insert)
    #     return str(result.inserted_id)
    #
    # def get_data(self, name: str):
    #     print(type(name))
    #     print(name)
    #     retrieved_document = self.collection.find_one({"name": name})
    #     if retrieved_document:
    #         return retrieved_document
    #     return None

    def save_image_to_gridfs(self, file_name: str, image_bytes: bytes):

        image_id = self.fs.put(image_bytes, filename=file_name)
        return image_id

    def get_image_from_gridfs_by_filename(self, pokemon_name : str):
        try:
            file = self.fs.find_one({"filename": pokemon_name})
            if file:
                return file.read()
            return None
        except Exception as e:
            raise e