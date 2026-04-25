from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()

from app.users.routes import router as users_router
from app.plants.routes import router as plants_router
from app.plants.identify import router as identify_router

app = FastAPI(title="PlantCare API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en local permite todo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router, prefix="/api")
app.include_router(plants_router, prefix="/api")
app.include_router(identify_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "PlantCare API funcionando"}