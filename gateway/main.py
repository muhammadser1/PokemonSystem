from fastapi import FastAPI
from controllers import Pokemon_Router, Trainer_Router, Pokemon_Image_Router

server = FastAPI()
server.include_router(Pokemon_Router.router)
server.include_router(Trainer_Router.router)
server.include_router(Pokemon_Image_Router.router)
