from enum import Enum

_WEIGHT_MAP = {
    "etc": 0,
    "Practice": 10,
    "Easy-": 30,
    "Easy": 40,
    "Easy+": 50,
    "Medium-": 60,
    "Medium": 70,
    "Medium+": 80,
    "Hard-": 90,
    "Hard": 100,
    "Hard+": 110,
    "VeryHard-": 120,
    "VeryHard": 130,
    "VeryHard+": 140,
    "Extreme-": 150,
    "Extreme": 160,
    "Extreme+": 170,
    "Hell": 180,
}

class Difficulty(str, Enum):
    ETC = "etc"
    PRACTICE = "Practice"
    EASYM = "Easy-"
    EASY = "Easy"
    EASYP = "Easy+"
    MEDIUMM = "Medium-"
    MEDIUM = "Medium"
    MEDIUMP = "Medium+"
    HARDM = "Hard-"
    HARD = "Hard"
    HARDP = "Hard+"
    VERY_HARDM = "VeryHard-"
    VERY_HARD = "VeryHard"
    VERY_HARDP = "VeryHard+"
    EXTREMEM = "Extreme-"
    EXTREME = "Extreme"
    EXTREMEP = "Extreme+"
    HELL = "Hell"

    @property
    def weight(self) -> int:
        return _WEIGHT_MAP.get(self.value, 999)
