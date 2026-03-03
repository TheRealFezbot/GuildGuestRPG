from datetime import datetime, timezone
from fastapi import HTTPException
from app.models.character import Character

# CHARACTERS

def calculate_power_level(hp: int, attack: int, defense: int) -> int:
    return 10 + attack + defense + hp // 2

def xp_for_next_level(level: int) -> int:
    return round(100 * (level ** 1.5)) 
    # TODO: Add max level cap

def get_current_stamina(character: Character) -> int:
    now = datetime.now(timezone.utc)
    elapsed_minutes = (now - character.stamina_updated_at.replace(tzinfo=timezone.utc)).total_seconds() / 60
    regen = int(elapsed_minutes / 3)
    current_stamina = min(100, character.stamina + regen)

    return current_stamina