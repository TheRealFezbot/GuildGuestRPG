from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.core.database import get_db
from app.schemas.zone import ZoneResponse
from app.crud.zone import get_zones_for_character, get_zone_progress
from app.crud.monster import get_monsters_for_zone
from app.core.dependencies import get_current_user
from app.crud.character import get_character_by_user_id
from app.schemas.monster import MonsterWithProgressResponse

router = APIRouter(prefix="/zones", tags=["zones"])

@router.get("/", response_model=list[ZoneResponse])
async def get_zones(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    character = get_character_by_user_id(db, current_user.id)
    return get_zones_for_character(db, character.id)

@router.get("/{zone_id}/monsters", response_model=list[MonsterWithProgressResponse])
async def get_monsters(zone_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    character = get_character_by_user_id(db, current_user.id)
    zone_progress = get_zone_progress(db, zone_id, character.id)

    if not zone_progress or not zone_progress.is_unlocked:
        raise HTTPException(status_code=403, detail="You don't have access to this zone")
    
    return get_monsters_for_zone(db, zone_id, character.id)