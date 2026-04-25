from pydantic import BaseModel, validator
from typing import Optional


class Plant(BaseModel):
    id: Optional[str] = None
    userId: str
    name: str
    species: Optional[str] = None
    category: Optional[str] = None
    wateringDays: Optional[int] = 1
    lastWatered: Optional[str] = None
    health: Optional[str] = "okay"
    image: Optional[str] = None

    @validator("wateringDays")
    def watering_days_must_be_positive(cls, v):
        if v is not None and v < 1:
            raise ValueError("wateringDays debe ser mayor a 0")
        return v


class PlantUpdate(BaseModel):
    """Solo los campos editables desde el formulario de planta."""
    name: Optional[str] = None
    species: Optional[str] = None
    category: Optional[str] = None
    wateringDays: Optional[int] = None
    image: Optional[str] = None

    @validator("wateringDays")
    def watering_days_must_be_positive(cls, v):
        if v is not None and v < 1:
            raise ValueError("wateringDays debe ser mayor a 0")
        return v