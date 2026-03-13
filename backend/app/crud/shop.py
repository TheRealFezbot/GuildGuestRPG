from sqlalchemy.orm import Session
import uuid

from app.models.shop_listings import ShopListings
from app.models.inventory import Inventory
from app.models.item import Item

def get_shop_listings(db: Session, zone_id: str):
    rows = db.query(ShopListings, Item)\
        .join(Item, ShopListings.item_id == Item.id)\
        .filter(ShopListings.zone_id == zone_id, ShopListings.is_active == True)\
        .all()
    result = []
    for listing, item in rows:
        item_data = {k: v for k, v in item.__dict__.items() if not k.startswith("_")}
        item_data["listing_id"] = listing.id
        item_data["stock"] = listing.stock
        result.append(item_data)
    return result

def buy_item(db: Session, zone_id: str, item_id: str, character):
    listing = db.query(ShopListings).filter(
        ShopListings.zone_id == zone_id,
        ShopListings.item_id == item_id,
        ShopListings.is_active == True,
    ).first()
    if not listing:
        return None, None, "Item not available in this shop"
    
    item = db.query(Item).filter(Item.id == item_id).first()

    if character.gold < item.buy_price:
        return None, None, "Not enough gold"
    
    already_owned = db.query(Inventory).filter(
        Inventory.character_id == character.id,
        Inventory.item_id == item_id,
    ).first()
    if already_owned:
        return None, None, "You already own this item"
    
    character.gold -= item.buy_price
    entry = Inventory(id=uuid.uuid4(), character_id=character.id, item_id=item_id)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry, item, None