from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.shop import ShopItemResponse, BuyResponse
from app.core.database import get_db
from app.crud.shop import get_shop_listings, buy_item
from app.core.dependencies import get_current_character

router = APIRouter(prefix="/shop", tags=["shop"])

@router.get("/{zone_id}", response_model=list[ShopItemResponse])
def get_shop_items(zone_id: str, db: Session = Depends(get_db), character = Depends(get_current_character)):
    return get_shop_listings(db, zone_id)

@router.post("/{zone_id}/buy/{item_id}", response_model=BuyResponse)
def buy_shop_item(zone_id: str, item_id: str, db: Session = Depends(get_db), character = Depends(get_current_character)):
    entry, item, error = buy_item(db, zone_id, item_id, character)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return BuyResponse(message="Purchase successful", item_name=item.name, gold_remaining=character.gold)