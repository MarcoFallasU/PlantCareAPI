from pydantic import BaseModel
from typing import Optional, List


class User(BaseModel):
    id: Optional[str] = None
    nombre: str
    apodo: str
    email: str
    image: Optional[str] = None
    descripcion: Optional[str] = None
    plantaFavorita: Optional[str] = None
    cumpleanos: Optional[str] = None
    racha: Optional[int] = 0
    cantidadAmigos: Optional[int] = 0
    privacidad: Optional[str] = "Público"
    categoriasPlantas: Optional[List[str]] = []
    createdAt: Optional[str] = None
    lastWateredDate: Optional[str] = None


class UserUpdate(BaseModel):
    nombre: Optional[str] = None
    apodo: Optional[str] = None
    descripcion: Optional[str] = None
    plantaFavorita: Optional[str] = None
    cumpleanos: Optional[str] = None
    image: Optional[str] = None