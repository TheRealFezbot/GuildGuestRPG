from app.core.database import SessionLocal
from app.models.zone import Zone

def seed_zones(db):
    zones = [
        {"name": "Whispering Forest", "description": "A misty woodland...",         "order": 1, "recommended_level_min": 1,  "recommended_level_max": 5},
        {"name": "Darkstone Caves",   "description": "Dark underground caverns...", "order": 2, "recommended_level_min": 5,  "recommended_level_max": 10},
        {"name": "Shattered Ruins",   "description": "Ancient crumbling ruins...",  "order": 3, "recommended_level_min": 10, "recommended_level_max": 16},
        {"name": "Ember Volcano",     "description": "A volcanic wasteland...",     "order": 4, "recommended_level_min": 16, "recommended_level_max": 22},
    ]
    
    for z in zones:
        if not db.query(Zone).filter(Zone.order == z["order"]).first():
            db.add(Zone(**z))
            print(f"Seeded {z['name']}")
        else:
            print(f"{z['name']} was already seeded, skipping...")
    
    db.commit()

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_zones(db)
    finally:
        db.close()