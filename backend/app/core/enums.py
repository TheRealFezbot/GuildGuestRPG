from enum import Enum

class ClassType(Enum):
    warrior = "warrior"
    mage = "mage"
    rogue = "rogue"
    ranger = "ranger"

class ItemRarity(Enum):
    common = "common"
    uncommon = "uncommon"
    rare = "rare"
    epic = "epic"
    legendary = "legendary"

class ItemType(Enum):
    weapon = "weapon"
    head = "head"
    chest = "chest"
    legs = "legs"
    offhand = "offhand"
    accessory = "accessory"

class PotionType(Enum):
    health = "health"
    attack = "attack"

class CombatResult(Enum):
    win = "win"
    lose = "lose"
    flee = "flee"