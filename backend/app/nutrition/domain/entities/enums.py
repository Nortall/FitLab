from enum import Enum


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class ActivityFactor(float, Enum):
    SEDENTARY = 1.2
    LIGHT = 1.375
    MODERATE = 1.55
    HIGH = 1.725
    EXTREME = 1.9
