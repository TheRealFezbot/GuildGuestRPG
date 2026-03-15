from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_character
from app.schemas.inventory import InventoryItemResponse
from app.crud.inventory import get_inventory, equip_item, unequip_item

router = APIRouter(prefix="/inventory", tags=["inventory"])

@router.get("/", response_model=list[InventoryItemResponse])
def get_inventory_item(db: Session = Depends(get_db), character = Depends(get_current_character)):
    return get_inventory(db, character.id)

@router.post("/{inventory_id}/equip")
def equip(inventory_id: str, db: Session = Depends(get_db), character = Depends(get_current_character)):
    _, error = equip_item(db, inventory_id, character)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return {"message": "Item equipped"}
    

@router.post("/{inventory_id}/unequip")
def unequip(inventory_id: str, db: Session = Depends(get_db), character = Depends(get_current_character)):
    _, error = unequip_item(db, inventory_id, character)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return {"message": "Item unequipped"}