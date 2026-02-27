from app.core.database import SessionLocal
from app.models.zone import Zone
from app.models.monster import Monster

def seed_monsters(db):
    zone1 = db.query(Zone).filter(Zone.order == 1).first()
    if not zone1:
        raise Exception("Zones must be seeded before monsters.")
    zone2 = db.query(Zone).filter(Zone.order == 2).first()
    if not zone2:
        raise Exception("Zones must be seeded before monsters.")
    zone3 = db.query(Zone).filter(Zone.order == 3).first()
    if not zone3:
        raise Exception("Zones must be seeded before monsters.")
    zone4 = db.query(Zone).filter(Zone.order == 4).first()
    if not zone4:
        raise Exception("Zones must be seeded before monsters.")
    

    monsters = [
    {"zone_id": zone1.id, "name": "Slime",        "order_in_zone": 1, "is_zone_boss": False, "base_hp": 30,  "base_attack": 4,  "base_defense": 1,  "base_xp_reward": 20,   "base_gold_min": 5,   "base_gold_max": 10},
    {"zone_id": zone1.id, "name": "Goblin",       "order_in_zone": 2, "is_zone_boss": False, "base_hp": 50,  "base_attack": 7,  "base_defense": 2,  "base_xp_reward": 30,   "base_gold_min": 8,   "base_gold_max": 15},
    {"zone_id": zone1.id, "name": "Wolf",         "order_in_zone": 3, "is_zone_boss": False, "base_hp": 70,  "base_attack": 9,  "base_defense": 3,  "base_xp_reward": 45,   "base_gold_min": 12,  "base_gold_max": 20},
    {"zone_id": zone1.id, "name": "Treant",       "order_in_zone": 4, "is_zone_boss": True,  "base_hp": 100, "base_attack": 12, "base_defense": 6,  "base_xp_reward": 70,   "base_gold_min": 20,  "base_gold_max": 35},
    {"zone_id": zone2.id, "name": "Bat",          "order_in_zone": 1, "is_zone_boss": False, "base_hp": 80,  "base_attack": 11, "base_defense": 4,  "base_xp_reward": 80,   "base_gold_min": 25,  "base_gold_max": 40},
    {"zone_id": zone2.id, "name": "Spider",       "order_in_zone": 2, "is_zone_boss": False, "base_hp": 110, "base_attack": 14, "base_defense": 5,  "base_xp_reward": 100,  "base_gold_min": 35,  "base_gold_max": 55},
    {"zone_id": zone2.id, "name": "Orc",          "order_in_zone": 3, "is_zone_boss": False, "base_hp": 150, "base_attack": 18, "base_defense": 8,  "base_xp_reward": 130,  "base_gold_min": 50,  "base_gold_max": 75},
    {"zone_id": zone2.id, "name": "Cave Troll",   "order_in_zone": 4, "is_zone_boss": True,  "base_hp": 220, "base_attack": 24, "base_defense": 12, "base_xp_reward": 180,  "base_gold_min": 80,  "base_gold_max": 120},
    {"zone_id": zone3.id, "name": "Skeleton",     "order_in_zone": 1, "is_zone_boss": False, "base_hp": 180, "base_attack": 22, "base_defense": 10, "base_xp_reward": 200,  "base_gold_min": 100, "base_gold_max": 150},
    {"zone_id": zone3.id, "name": "Wraith",       "order_in_zone": 2, "is_zone_boss": False, "base_hp": 200, "base_attack": 28, "base_defense": 8,  "base_xp_reward": 240,  "base_gold_min": 130, "base_gold_max": 190},
    {"zone_id": zone3.id, "name": "Golem",        "order_in_zone": 3, "is_zone_boss": False, "base_hp": 300, "base_attack": 32, "base_defense": 20, "base_xp_reward": 300,  "base_gold_min": 175, "base_gold_max": 250},
    {"zone_id": zone3.id, "name": "Lich",         "order_in_zone": 4, "is_zone_boss": True,  "base_hp": 400, "base_attack": 40, "base_defense": 18, "base_xp_reward": 400,  "base_gold_min": 250, "base_gold_max": 380},
    {"zone_id": zone4.id, "name": "Fire Imp",     "order_in_zone": 1, "is_zone_boss": False, "base_hp": 300, "base_attack": 38, "base_defense": 15, "base_xp_reward": 450,  "base_gold_min": 300, "base_gold_max": 450},
    {"zone_id": zone4.id, "name": "Lava Serpent", "order_in_zone": 2, "is_zone_boss": False, "base_hp": 420, "base_attack": 48, "base_defense": 20, "base_xp_reward": 580,  "base_gold_min": 400, "base_gold_max": 580},
    {"zone_id": zone4.id, "name": "Infernal Orc", "order_in_zone": 3, "is_zone_boss": False, "base_hp": 560, "base_attack": 58, "base_defense": 28, "base_xp_reward": 720,  "base_gold_min": 520, "base_gold_max": 750},
    {"zone_id": zone4.id, "name": "Elder Dragon", "order_in_zone": 4, "is_zone_boss": True,  "base_hp": 800, "base_attack": 75, "base_defense": 40, "base_xp_reward": 1000, "base_gold_min": 750, "base_gold_max": 1200},
]
    
    for m in monsters:
        exists = db.query(Monster).filter(
            Monster.zone_id == m["zone_id"],
            Monster.order_in_zone == m["order_in_zone"]
        ).first()

        if not exists:
            db.add(Monster(**m))
            print(f"seeded {m['name']}")
        else:
            print(f"{m['name']} already seeded, skipping...")
    
    db.commit()

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_monsters(db)
    finally:
        db.close()

