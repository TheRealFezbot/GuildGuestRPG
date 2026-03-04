from datetime import datetime, timezone

from app.core.constants import MAX_STAMINA, STAMINA_REGEN_MINUTES, STAMINA_REGEN_AMOUNT
from app.models.character import Character

# CHARACTERS

def calculate_power_level(hp: int, attack: int, defense: int) -> int:
    # attack weighted double since it tends to matter most in combat
    return 10 + attack * 2 + defense + hp // 3

def xp_for_next_level(level: int) -> int:
    return round(100 * (level ** 1.5))
    # TODO: Add max level cap

def get_current_stamina(character: Character) -> int:
    # stamina isn't stored live - we store the last known value + timestamp and calculate regen on the fly
    now = datetime.now(timezone.utc)
    elapsed_minutes = (now - character.stamina_updated_at.replace(tzinfo=timezone.utc)).total_seconds() / 60
    regen = int(elapsed_minutes / STAMINA_REGEN_MINUTES) * STAMINA_REGEN_AMOUNT
    current_stamina = min(MAX_STAMINA, character.stamina + regen)

    return current_stamina