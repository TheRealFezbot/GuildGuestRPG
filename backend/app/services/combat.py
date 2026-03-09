import random

from app.models.character import Character
from app.core.game import calculate_power_level
from app.core.enums import ClassType

def clamp(value, min_val, max_val):
    return max(min_val, min(max_val, value))

def simulate_combat(character: Character, monster: dict, level_num: int) -> dict:
    level_data = next((l for l in monster["levels"] if l.level == level_num), None)
    if not level_data:
        raise ValueError(f"Level {level_num} not found for monster")
    
    # scale base stats by the level multipliers (levels 1-5 make the monster progressively stronger)
    scaled_monster_stats = {
        "hp": monster["base_hp"] * level_data.hp_multiplier,
        "attack": monster["base_attack"] * level_data.attack_multiplier,
        "defense": monster["base_defense"] * level_data.defense_multiplier,
    }

    monster_power = calculate_power_level(
        round(scaled_monster_stats["hp"]),
        round(scaled_monster_stats["attack"]),
        round(scaled_monster_stats["defense"]),
    )

    player_hp = character.max_hp
    # rogue gets higher crit and dodge caps as a class passive
    crit_cap = 0.50 if character.class_type == ClassType.rogue else 0.40
    crit_chance = clamp(0.10 + character.crit_bonus, 0, crit_cap)
    base_damage = max(1, character.attack - (scaled_monster_stats["defense"] / 2))
    dodge_cap = 0.40 if character.class_type == ClassType.rogue else 0.35
    dodge_chance = clamp(0.05 + (character.defense / 200) + character.dodge_bonus, 0.05, dodge_cap)

    # hit chance scales with the power level ratio - ratio > 1 means we outpower the monster
    # stronger character hits more often and is harder to hit back
    ratio = character.power_level / max(monster_power, 1)
    hit_chance = clamp(0.85 + (ratio - 1) * 0.1 + character.hit_bonus, 0.50, 0.95)
    monster_hit_chance = clamp(0.85 - (ratio - 1) * 0.1, 0.50, 0.95)
    
    monster_hp = round(scaled_monster_stats["hp"])
    monster_base_damage = max(1, scaled_monster_stats["attack"] - (character.defense / 2))
    monster_dodge_chance = clamp(0.05 + (scaled_monster_stats["defense"] / 200), 0.05, 0.20)
    
    log = []
    turn = 0
    damage_dealt = 0
    damage_taken = 0
    winner = None

    while player_hp > 0 and monster_hp > 0:
        turn += 1
        
        # player attack
        if random.random() > hit_chance:
            log.append(f"Turn {turn}: {character.name} misses!")
        else:
            if random.random() < monster_dodge_chance:
                log.append(f"Turn {turn}: {monster["name"]} dodged the attack!")
            else:
                is_crit = random.random() < crit_chance
                damage = round(base_damage * (1.5 if is_crit else 1.0) * random.uniform(0.8, 1.2))

                monster_hp -= damage
                damage_dealt += damage
                log.append(f"Turn {turn}: {'Critical hit! ' if is_crit else ''}{character.name} attacks {monster["name"]} for {damage} damage!")
                log.append(f"{monster["name"]} has {max(0, monster_hp)} health left.")
        
        # monster attack (only if still allive) 
        if monster_hp > 0:
            if random.random() > monster_hit_chance:
                log.append(f"Turn {turn}: {monster['name']} misses!")
            else:
                if random.random() < dodge_chance:
                    log.append(f"Turn {turn}: {character.name} dodged the attack!")
                else:
                    damage = round(monster_base_damage * random.uniform(0.8, 1.2))

                    player_hp -= damage
                    damage_taken += damage
                    log.append(f"Turn {turn}: {monster["name"]} attacks {character.name} for {damage} damage!")
                    log.append(f"{character.name} has {max(0, player_hp)} health left.")
    
    if monster_hp <= 0:
        winner = "player"
        xp_gained = round(monster["base_xp_reward"] * level_data.xp_multiplier)
        gold_gained = round(random.randint(monster["base_gold_min"], monster["base_gold_max"]) * level_data.gold_multiplier)
        if character.class_type == ClassType.mage:
            gold_gained = round(gold_gained * 1.15)
        log.append(f"{character.name} has won!")
    else:
        winner = "monster"
        xp_gained = 0
        gold_gained = 0
        log.append(f"{monster["name"]} has won!")

    return {
        "winner": winner,
        "xp_gained": xp_gained,
        "gold_gained": gold_gained,
        "item_dropped_id": None, # TODO: drop table
        "turns_taken": turn,
        "damage_dealt": damage_dealt,
        "damage_taken": damage_taken,
        "combat_text": log,
    }  


