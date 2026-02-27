from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, characters


app = FastAPI()
app.include_router(auth.router)
app.include_router(characters.router)

origins = ["http://localhost:5173"]

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