from fastapi import APIRouter
from typing import Optional
from app.plants.models import Plant, PlantUpdate
from app.plants import service

router = APIRouter(prefix="/plants", tags=["Plants"])


@router.get("")
async def get_plants(userId: Optional[str] = None):
    """Sin userId devuelve todas. Con ?userId=<id> filtra por usuario."""
    if userId:
        return service.get_plants_by_user(userId)
    return service.get_all_plants()


@router.get("/{plant_id}")
async def get_plant(plant_id: str):
    return service.get_plant(plant_id)


@router.post("")
async def create_plant(plant: Plant):
    return service.create_plant(plant)


@router.put("/{plant_id}")
async def update_plant(plant_id: str, plant: PlantUpdate):
    return service.update_plant(plant_id, plant)


@router.delete("/{plant_id}")
async def delete_plant(plant_id: str):
    return service.delete_plant(plant_id)