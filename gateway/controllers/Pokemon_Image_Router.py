import base64
import httpx
from typing import Dict, Any

import requests
from fastapi import APIRouter, Query, HTTPException,Request
from class_gateway import ClassGateway
from fastapi.responses import StreamingResponse
import io
from redis_manager import get_redis

router = APIRouter(prefix='/pokemon/images', tags=['Pokemon Images'])
gateway_instance = ClassGateway()
redis_client = get_redis()

@router.get("/{pokemon_name}")
def get_pokemon_image(request: Request,pokemon_name: str):
    full_path = request.url.path

    img_bytes_response = gateway_instance.get_image_of_pokemon(pokemon_name)
    if img_bytes_response.status_code ==404:
        raise HTTPException(status_code=404, detail="No image found for the given Pokemon")
    encoded_data = base64.b64encode(img_bytes_response.content).decode('utf-8')
    redis_client.set_value(full_path, encoded_data)
    return StreamingResponse(io.BytesIO(img_bytes_response.content), media_type="image/png")
