from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.crud.character import get_character_by_id, get_character_by_name, get_character_by_user_id, create_character
from app.schemas.character import CharacterCreate, CharacterResponse, CharacterPublic
from app.core.dependencies import get_current_user
from app.core.game import get_current_stamina
from app.core.constants import BASE_STATS
from app.core.redis import get_stamina
from app.core.database import get_db
from app.models.user import User

router = APIRouter(prefix="/characters", tags=["characters"])

@router.post("/", response_model=CharacterResponse)
async def create(data: CharacterCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if get_character_by_name(db, data.name):
        raise HTTPException(status_code=400, detail="That name is already taken.")
    
    character = create_character(db, current_user.id, data.name, data.class_type)

    return character

@router.get("/me", response_model=CharacterResponse)
async def get_me(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    character = get_character_by_user_id(db, current_user.id)
    if not character:
        raise HTTPException(status_code=404, detail="No character found")
    cached = get_stamina(character.id)
    if cached:
        character.stamina = cached["stamina"]
        character.stamina_updated_at = datetime.fromisoformat(cached["updated_at"])
    character.stamina = get_current_stamina(character)

    return character

@router.get("/classes")
def get_class_stats():
    return BASE_STATS

@router.get("/{character_id}", response_model=CharacterPublic)
async def get_character(character_id: str, db: Session = Depends(get_db)):
    character = get_character_by_id(db, character_id)
    if not character:
        raise HTTPException(status_code=404, detail="No character found")
    
    return character