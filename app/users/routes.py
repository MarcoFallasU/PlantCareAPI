from fastapi import APIRouter
from app.users.models import User, UserUpdate
from app.users import service

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{user_id}")
async def get_user(user_id: str):
    return service.get_user(user_id)
    
@router.get("")
async def get_all_users():
    return service.get_all_users()

@router.post("")
async def create_user(user: User):
    return service.create_user(user)


@router.put("/{user_id}")
async def update_user(user_id: str, user: UserUpdate):
    return service.update_user(user_id, user)


@router.delete("/{user_id}")
async def delete_user(user_id: str):
    return service.delete_user(user_id)

@router.post("/{user_id}/check-streak")
async def check_streak(user_id: str):
    doc = db.collection("users").document(user_id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    data          = doc.to_dict()
    racha_actual  = data.get("racha", 0)
    last_date_str = data.get("lastWateredDate")
    today         = date.today()

    if not last_date_str:
        return {"racha": racha_actual, "lastWateredDate": None}

    last_date = date.fromisoformat(last_date_str)
    days_diff = (today - last_date).days

    if days_diff > 1:
        db.collection("users").document(user_id).update({"racha": 0})
        return {"racha": 0, "lastWateredDate": last_date_str}

    return {"racha": racha_actual, "lastWateredDate": last_date_str}


@router.post("/{user_id}/water")
async def register_watering(user_id: str):
    doc = db.collection("users").document(user_id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    data          = doc.to_dict()
    racha_actual  = data.get("racha", 0)
    last_date_str = data.get("lastWateredDate")
    today_str     = date.today().isoformat()

    if last_date_str == today_str:
        return {"racha": racha_actual, "incremented": False}

    nueva_racha = racha_actual + 1
    db.collection("users").document(user_id).update({
        "racha":           nueva_racha,
        "lastWateredDate": today_str,
    })
    return {"racha": nueva_racha, "incremented": True}