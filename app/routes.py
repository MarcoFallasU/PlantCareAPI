from fastapi import APIRouter, HTTPException
from app.firebase_config import db
from app.models import User, Plant
from datetime import date

router = APIRouter()


@router.get("/users/{user_id}")
async def get_user(user_id: str):
    doc = db.collection("users").document(user_id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"id": doc.id, **doc.to_dict()}

@router.post("/users")
async def create_user(user: User):
    data = user.dict(exclude={"id"})
    ref = db.collection("users").add(data)
    return {"id": ref[1].id, **data}

@router.put("/users/{user_id}")
async def update_user(user_id: str, user: User):
    data = user.dict(exclude={"id"}, exclude_none=True)
    db.collection("users").document(user_id).update(data)
    return {"id": user_id, **data}

@router.delete("/users/{user_id}")
async def delete_user(user_id: str):
    db.collection("users").document(user_id).delete()
    return {"message": f"Usuario {user_id} eliminado"}



@router.get("/plants")
async def get_plants(userId: str):
    docs = db.collection("plants").where("userId", "==", userId).stream()
    return [{"id": doc.id, **doc.to_dict()} for doc in docs]

@router.get("/plants/{plant_id}")
async def get_plant(plant_id: str):
    doc = db.collection("plants").document(plant_id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Planta no encontrada")
    return {"id": doc.id, **doc.to_dict()}

@router.post("/plants")
async def create_plant(plant: Plant):
    data = plant.dict(exclude={"id"})
    ref = db.collection("plants").add(data)
    return {"id": ref[1].id, **data}

@router.put("/plants/{plant_id}")
async def update_plant(plant_id: str, plant: Plant):
    data = plant.dict(exclude={"id"}, exclude_none=True)
    db.collection("plants").document(plant_id).update(data)
    return {"id": plant_id, **data}

@router.delete("/plants/{plant_id}")
async def delete_plant(plant_id: str):
    db.collection("plants").document(plant_id).delete()
    return {"message": f"Planta {plant_id} eliminada"}