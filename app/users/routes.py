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