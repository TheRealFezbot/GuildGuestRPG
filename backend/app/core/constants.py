from app.core.enums import ClassType

# SECURITY
ALLOWED_SPECIAL_CHARS = "!@#$%^&*(\{\}\\/><.,\"':;)-_+=?~[]|"
MIN_AGE = 13

# CHARACTERS
BASE_STATS = {
    ClassType.warrior: {
        "hp": 120,
        "attack": 10,
        "defense": 8,
    },
    ClassType.mage: {
        "hp": 80,
        "attack": 15,
        "defense": 4,
    },
    ClassType.rogue: {
        "hp": 100,
        "attack": 12,
        "defense": 5,
    },
    ClassType.ranger: {
        "hp": 100,
        "attack": 11,
        "defense": 6,
    },
}
