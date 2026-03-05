from app.core.enums import ClassType

# SECURITY
ALLOWED_SPECIAL_CHARS = "!@#$%^&*(\{\}\\/><.,\"':;)-_+=?~[]|"
MIN_AGE = 13

# USERS
MIN_USERNAME_LENGTH = 5
MAX_USERNAME_LENGTH = 20

# CHARACTERS
MIN_CHARACTER_NAME_LENGTH = 3
MAX_CHARACTER_NAME_LENGTH = 20


BASE_STATS = {
    ClassType.warrior: { "hp": 120, "attack": 10, "defense": 8, "crit_bonus": 0.0, "dodge_bonus": 0.0 },
    ClassType.mage:    { "hp": 80,  "attack": 15, "defense": 4, "crit_bonus": 0.0, "dodge_bonus": 0.0 },
    ClassType.rogue:   { "hp": 100, "attack": 12, "defense": 5, "crit_bonus": 0.05, "dodge_bonus": 0.08 },
    ClassType.ranger:  { "hp": 100, "attack": 11, "defense": 6, "crit_bonus": 0.0, "dodge_bonus": 0.0 },
}

STAT_GROWTH = {
    ClassType.warrior: {"max_hp": 12, "attack": 2, "defense": 2},
    ClassType.mage: {"max_hp": 6, "attack": 3, "defense": 1},
    ClassType.rogue: {"max_hp": 8, "attack": 2, "defense": 1},
    ClassType.ranger: {"max_hp": 10, "attack": 2, "defense": 1},
}

# STAMINA
MAX_STAMINA = 100
STAMINA_REGEN_MINUTES = 3 
STAMINA_REGEN_AMOUNT = 5
STAMINA_COST = 5
STAMINA_COST_BOSS = 10

# MONSTERS
MONSTER_UNLOCK_THRESHOLD = 3 # Highest level beaten needed to unlock the next monster
ZONE_UNLOCK_THRESHOLD = 5 # Highest level beaten on Zone Boss to unlock the next zone