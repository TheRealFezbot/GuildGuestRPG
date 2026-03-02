# CHARACTERS

def calculate_power_level(hp: int, attack: int, defense: int) -> int:
    return 10 + attack + defense + hp // 2

def xp_for_next_level(level: int) -> int:
    return round(100 * (level ** 1.5)) 
    # TODO: Add max level cap