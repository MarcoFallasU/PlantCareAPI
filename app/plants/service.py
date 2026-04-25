from fastapi import HTTPException
from app.firebase_config import db
from app.plants.models import Plant, PlantUpdate


COLLECTION = "plants"

def get_all_plants() -> list:
    docs = db.collection(COLLECTION).stream()
    return [{"id": doc.id, **doc.to_dict()} for doc in docs]


def get_plants_by_user(user_id: str) -> list:
    docs = db.collection(COLLECTION).where("userId", "==", user_id).stream()
    return [{"id": doc.id, **doc.to_dict()} for doc in docs]


def get_plant(plant_id: str) -> dict:
    doc = db.collection(COLLECTION).document(plant_id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Planta no encontrada")
    return {"id": doc.id, **doc.to_dict()}


def create_plant(plant: Plant) -> dict:
    data = plant.dict(exclude={"id"})
    ref = db.collection(COLLECTION).add(data)
    return {"id": ref[1].id, **data}


def update_plant(plant_id: str, plant: PlantUpdate) -> dict:
    doc = db.collection(COLLECTION).document(plant_id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Planta no encontrada")

    data = plant.dict(exclude_none=True)
    if not data:
        raise HTTPException(status_code=400, detail="No se enviaron campos para actualizar")

    db.collection(COLLECTION).document(plant_id).update(data)
    return {"id": plant_id, **data}


def delete_plant(plant_id: str) -> dict:
    doc = db.collection(COLLECTION).document(plant_id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Planta no encontrada")
    db.collection(COLLECTION).document(plant_id).delete()
    return {"message": f"Planta {plant_id} eliminada"}