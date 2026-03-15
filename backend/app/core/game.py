from datetime import datetime, timezone

from app.core.constants import MAX_STAMINA, STAMINA_REGEN_MINUTES, STAMINA_REGEN_AMOUNT
from app.models.character import Character
from app.models.item import Item

# CHARACTERS

def calculate_power_level(hp: int, attack: int, defense: int) -> int:
    # attack weighted double since it tends to matter most in combat
    return 10 + attack * 2 + defense + hp // 3

def apply_equipment_stats(character: Character, item: Item, equip: bool = True):
    modifier = 1 if equip else -1
    character.attack += item.attack_bonus * modifier 
    character.defense += item.defense_bonus * modifier
    character.max_hp += item.hp_bonus * modifier
    if not equip and character.hp > character.max_hp:
        character.hp = character.max_hp
    # TODO add item bonuses for crit and dodge
    character.power_level = calculate_power_level(character.max_hp, character.attack, character.defense)

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