# app/plants/identify.py
import base64
import httpx
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
import os
import json

router = APIRouter(prefix="/plants", tags=["Identify"])


class PlantIdentificationResult(BaseModel):
    name: str
    scientificName: str
    confidence: int
    description: str
    careLevel: str
    sunlight: str
    water: str
    humidity: str
    isPlant: bool


SYSTEM_PROMPT = """Eres un botánico experto. Analiza la imagen y responde ÚNICAMENTE con un JSON válido sin markdown, sin bloques de código, sin texto adicional.

Si la imagen contiene una planta:
{"isPlant": true, "name": "Nombre común en español", "scientificName": "Nombre científico", "confidence": <60-99>, "description": "Descripción breve en español, máximo 2 oraciones", "careLevel": "Easy" o "Moderate" o "Expert", "sunlight": "descripción", "water": "descripción", "humidity": "descripción"}

Si NO contiene una planta:
{"isPlant": false, "name": "", "scientificName": "", "confidence": 0, "description": "No se detectó ninguna planta.", "careLevel": "Easy", "sunlight": "", "water": "", "humidity": ""}"""


@router.post("/identify")
async def identify_plant(file: UploadFile = File(...)):
    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY no configurada")

    image_bytes = await file.read()
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")
    mime_type = file.content_type or "image/jpeg"

    payload = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": SYSTEM_PROMPT},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{image_b64}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 512,
        "temperature": 0.2,
    }

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            json=payload,
            headers={"Authorization": f"Bearer {api_key}"}
        )

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail=f"Groq error: {response.text}")

    try:
        text = response.json()["choices"][0]["message"]["content"].strip()
        # Limpiar por si el modelo agrega markdown
        text = text.replace("```json", "").replace("```", "").strip()
        data = json.loads(text)
        return PlantIdentificationResult(**data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parseando respuesta: {e}")