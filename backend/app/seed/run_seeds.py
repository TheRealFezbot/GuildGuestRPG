from app.core.database import SessionLocal
from app.seed.seed_zones import seed_zones
from app.seed.seed_monsters import seed_monsters
from app.seed.seed_monster_levels import seed_monster_levels

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_zones(db)
        seed_monsters(db)
        seed_monster_levels(db)
        print("All seeds complete.")
    finally:
        db.close()