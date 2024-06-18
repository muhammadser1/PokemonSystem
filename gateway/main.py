import base64
from typing import Callable

from fastapi import FastAPI, Request, Response
from controllers import Pokemon_Router, Trainer_Router, Pokemon_Image_Router
import time
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
import io
from redis_class import RedisClient

server = FastAPI()
server.include_router(Pokemon_Router.router)
server.include_router(Trainer_Router.router)
server.include_router(Pokemon_Image_Router.router)
redis_client = RedisClient(host='redis', port=6379, db=0)
#


@server.middleware("http")
async def add_process_time_header(request: Request, call_next: Callable[[Request], Response]) -> Response:
    start_time = time.time()
    path = request.url.path
    if request.url.query:
        path = request.url.path + "?" + request.url.query
    if request.method == "GET":
        cached_data = redis_client.get_(path)
        if cached_data:
            if "/pokemon/images" in path:
                cached_data = base64.b64decode(cached_data)
                print("Redis Cache Hit")
                return StreamingResponse(io.BytesIO(cached_data), media_type="image/png")
            print("main:")
            print(path)
            print("Redis Cache Hit")
            cached_data = jsonable_encoder(cached_data)
            return JSONResponse(content=cached_data)

    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
