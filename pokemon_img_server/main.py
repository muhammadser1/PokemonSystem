import base64

from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from constants import pokemonImg
from schema import Image
from utils.read_json import read_json
from models.mongo_db import get_db
import requests
from fastapi.responses import StreamingResponse
import io

server = FastAPI()


@server.post("/add_img/")
def add_data_to_db(img:Image,db=Depends(get_db)):
    decoded_image = base64.b64decode(img.bytes)
    db.save_image_to_gridfs(img.name, decoded_image)
    return {"message": "Image saved to database"}

@server.get("/get_img")
def get_image_from_gridfs(pokemon_name: str, db=Depends(get_db)):
    image_bytes = db.get_image_from_gridfs_by_filename(pokemon_name)
    if image_bytes is None:
        raise HTTPException(status_code=404, detail="No image found for the given Pokemon")

    return StreamingResponse(io.BytesIO(image_bytes), media_type="image/png")

@server.post("/migration")
def migration_data(db=Depends(get_db)):
    json_data=read_json()
    pokemons_names = [0]
    for pokemon in json_data:
        pokemons_names.append(pokemon["name"])

    for i in range(1,152):
        img=requests.get(f"{pokemonImg}{i}.png")
        img_bytes=img.content
        db.save_image_to_gridfs(pokemons_names[i],img_bytes)
