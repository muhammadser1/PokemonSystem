from fastapi import FastAPI
from controllers import pokemon,trainer

server = FastAPI()
server.include_router(pokemon.router)
server.include_router(trainer.router)




