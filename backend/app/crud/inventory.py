from sqlalchemy.orm import Session
import uuid

from app.core.game import apply_equipment_stats
from app.models.inventory import Inventory
from app.models.character import Character
from app.models.item import Item

def get_inventory(db: Session, character_id: uuid):
    rows = db.query(Inventory, Item)\
        .join(Item, Inventory.item_id == Item.id)\
        .filter(Inventory.character_id == character_id)\
        .all()
    result = []
    for inventory, item in rows:
        item_data = {k: v for k, v in item.__dict__.items() if not k.startswith("_")}
        item_data["inventory_id"] = inventory.id
        item_data["equipped_slot"] = inventory.equipped_slot
        result.append(item_data)
    return result

def equip_item(db: Session, inventory_id: uuid, character: Character):
    row = db.query(Inventory).filter(
        Inventory.id == inventory_id,
        Inventory.character_id == character.id,
    ).first()
    if not row:
        return None, "Item not found in inventory"
    
    item = db.query(Item).filter(Item.id == row.item_id).first()

    prev_equiped = db.query(Inventory).filter(
        Inventory.character_id == character.id,
        Inventory.equipped_slot == item.type,
        Inventory.id != inventory_id,
    ).first()
    if prev_equiped:
        prev_item = db.query(Item).filter(Item.id == prev_equiped.item_id).first()
        apply_equipment_stats(character, prev_item, equip=False)
        prev_equiped.equipped_slot = None
    
    row.equipped_slot = item.type
    apply_equipment_stats(character, item, equip=True)
    db.commit()
    return row, None

def unequip_item(db: Session, inventory_id: uuid, character: Character):
    row = db.query(Inventory).filter(
        Inventory.id == inventory_id,
        Inventory.character_id == character.id,
    ).first()
    if not row:
        return None, "Item not found in inventory"
    
    item = db.query(Item).filter(Item.id == row.item_id).first()
    
    row.equipped_slot = None
    apply_equipment_stats(character, item, equip=False)
    db.commit()

    return row, None