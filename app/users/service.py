from fastapi import HTTPException
from app.firebase_config import db
from app.users.models import User, UserUpdate


COLLECTION = "users"

def get_all_users() -> list:
    docs = db.collection(COLLECTION).stream()
    return [{"id": doc.id, **doc.to_dict()} for doc in docs]

def get_user(user_id: str) -> dict:
    doc = db.collection(COLLECTION).document(user_id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"id": doc.id, **doc.to_dict()}


def create_user(user: User) -> dict:
    data = user.dict(exclude={"id"})
    ref = db.collection(COLLECTION).add(data)
    return {"id": ref[1].id, **data}


def update_user(user_id: str, user: UserUpdate) -> dict:
    # Verifica que el documento existe antes de actualizar
    doc = db.collection(COLLECTION).document(user_id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    data = user.dict(exclude_none=True)
    if not data:
        raise HTTPException(status_code=400, detail="No se enviaron campos para actualizar")

    db.collection(COLLECTION).document(user_id).update(data)
    return {"id": user_id, **data}


def delete_user(user_id: str) -> dict:
    doc = db.collection(COLLECTION).document(user_id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.collection(COLLECTION).document(user_id).delete()
    return {"message": f"Usuario {user_id} eliminado"}