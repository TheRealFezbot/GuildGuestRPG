from app.models.monster_level import MonsterLevel
from app.core.database import SessionLocal
from app.models.monster import Monster

LEVEL_MULTIPLIERS = [
    {"level": 1, "hp_multiplier": 1.0, "attack_multiplier": 1.0, "defense_multiplier": 1.0, "xp_multiplier": 1.0, "gold_multiplier": 1.0, "drop_chance_bonus": 0.00},
    {"level": 2, "hp_multiplier": 1.3, "attack_multiplier": 1.2, "defense_multiplier": 1.2, "xp_multiplier": 1.4, "gold_multiplier": 1.3, "drop_chance_bonus": 0.02},
    {"level": 3, "hp_multiplier": 1.6, "attack_multiplier": 1.4, "defense_multiplier": 1.4, "xp_multiplier": 1.8, "gold_multiplier": 1.6, "drop_chance_bonus": 0.04},
    {"level": 4, "hp_multiplier": 2.0, "attack_multiplier": 1.7, "defense_multiplier": 1.7, "xp_multiplier": 2.3, "gold_multiplier": 2.0, "drop_chance_bonus": 0.06},
    {"level": 5, "hp_multiplier": 2.5, "attack_multiplier": 2.0, "defense_multiplier": 2.0, "xp_multiplier": 3.0, "gold_multiplier": 2.5, "drop_chance_bonus": 0.08},
]

def seed_monster_levels(db):
    monsters = db.query(Monster).all()
    if not monsters:
        raise Exception("Monsters must be seeded before monster levels.")

    for monster in monsters:
        for multi in LEVEL_MULTIPLIERS:
            exists = db.query(MonsterLevel).filter(
            MonsterLevel.monster_id == monster.id,
            MonsterLevel.level == multi["level"]
            ).first()

            if not exists:
                db.add(MonsterLevel(monster_id = monster.id, **multi))
                print(f"seeded {monster.name} level {multi['level']}")
            else:
                print(f"{monster.name} level {multi['level']} already seeded, skipping...")
    
    db.commit()

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_monster_levels(db)
    finally:
        db.close()