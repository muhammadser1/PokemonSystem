import base64
import httpx
from typing import Dict, Any

import requests
from fastapi import APIRouter, Query, HTTPException
from class_gateway import ClassGateway
from fastapi.responses import StreamingResponse
import io

router = APIRouter(prefix='/pokemon/images', tags=['Pokemon Images'])
gateway_instance = ClassGateway()


@router.get("/{pokemon_name}")
def get_pokemon_image(pokemon_name: str):
    img_bytes_response = gateway_instance.get_image_of_pokemon(pokemon_name)
    if img_bytes_response.status_code ==404:
        raise HTTPException(status_code=404, detail="No image found for the given Pokemon")
    return StreamingResponse(io.BytesIO(img_bytes_response.content), media_type="image/png")
