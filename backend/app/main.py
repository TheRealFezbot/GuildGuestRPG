from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import auth, characters, zones, combat, shop, inventory


app = FastAPI()
app.include_router(auth.router)
app.include_router(characters.router)
app.include_router(zones.router)
app.include_router(combat.router)
app.include_router(shop.router)
app.include_router(inventory.router)

origins = settings.cors_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "OK"}