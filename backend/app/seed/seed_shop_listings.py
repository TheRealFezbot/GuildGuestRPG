from app.core.database import SessionLocal
from app.models.zone import Zone
from app.models.item import Item
from app.models.shop_listings import ShopListings

SHOP_ITEMS_BY_ZONE = {
    1: [
        # Warrior - Ironbark
        "Ironbark Sword", "Ironbark Breastplate", "Ironbark Legguards", "Ironbark Helm", "Ironbark Shield",
        # Mage - Mossveil
        "Mossveil Staff", "Mossveil Robe", "Mossveil Leggings", "Mossveil Hood", "Mossveil Tome",
        # Rogue - Shadowleaf
        "Shadowleaf Dagger", "Shadowleaf Vest", "Shadowleaf Breeches", "Shadowleaf Cowl", "Shadowleaf Shiv",
        # Ranger - Pinewood
        "Pinewood Bow", "Pinewood Jerkin", "Pinewood Leggings", "Pinewood Hood", "Pinewood Quiver",
        # Universal
        "Woodsman's Charm",
    ],
    2: [
        # Warrior - Stonewall
        "Stonewall Sword", "Stonewall Chestplate", "Stonewall Legplates", "Stonewall Helmet", "Stonewall Shield",
        # Mage - Gloomstone
        "Gloomstone Staff", "Gloomstone Robe", "Gloomstone Leggings", "Gloomstone Cowl", "Gloomstone Tome",
        # Rogue - Obsidian
        "Obsidian Dagger", "Obsidian Vest", "Obsidian Breeches", "Obsidian Cowl", "Obsidian Shiv",
        # Ranger - Bat-hide
        "Bat-hide Bow", "Bat-hide Jerkin", "Bat-hide Legwraps", "Bat-hide Hood", "Bat-hide Quiver",
        # Universal
        "Cave Pendant",
    ],
    3: [
        # Warrior - Ruinplate
        "Ruinplate Sword", "Ruinplate Chestplate", "Ruinplate Legguards", "Ruinplate Helm", "Ruinplate Shield",
        # Mage - Arcane Shard
        "Arcane Shard Staff", "Arcane Shard Robe", "Arcane Shard Leggings", "Arcane Shard Hood", "Arcane Shard Tome",
        # Rogue - Phantom
        "Phantom Dagger", "Phantom Vest", "Phantom Breeches", "Phantom Cowl", "Phantom Shiv",
        # Ranger - Galeshot
        "Galeshot Bow", "Galeshot Jerkin", "Galeshot Legwraps", "Galeshot Hood", "Galeshot Quiver",
        # Universal
        "Shard Pendant",
    ],
    4: [
        # Warrior - Emberlord
        "Emberlord Sword", "Emberlord Chestplate", "Emberlord Legguards", "Emberlord Helm", "Emberlord Shield",
        # Mage - Cinderweave
        "Cinderweave Staff", "Cinderweave Robe", "Cinderweave Leggings", "Cinderweave Hood", "Cinderweave Tome",
        # Rogue - Ashen
        "Ashen Dagger", "Ashen Vest", "Ashen Breeches", "Ashen Cowl", "Ashen Shiv",
        # Ranger - Smoldering
        "Smoldering Bow", "Smoldering Jerkin", "Smoldering Legwraps", "Smoldering Hood", "Smoldering Quiver",
        # Universal
        "Volcano Heart",
    ],
}


def seed_shop_listings(db):
    for zone_order, item_names in SHOP_ITEMS_BY_ZONE.items():
        zone = db.query(Zone).filter(Zone.order == zone_order).first()
        if not zone:
            raise Exception(f"Zone {zone_order} must be seeded before shop listings.")

        for name in item_names:
            item = db.query(Item).filter(Item.name == name).first()
            if not item:
                print(f"  Item '{name}' not found, skipping...")
                continue

            exists = db.query(ShopListings).filter(
                ShopListings.zone_id == zone.id,
                ShopListings.item_id == item.id,
            ).first()

            if not exists:
                db.add(ShopListings(zone_id=zone.id, item_id=item.id, is_active=True, stock=None))
                print(f"  Seeded listing: {name} (zone {zone_order})")
            else:
                print(f"  Already seeded: {name} (zone {zone_order}), skipping...")

    db.commit()


if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_shop_listings(db)
    finally:
        db.close()
