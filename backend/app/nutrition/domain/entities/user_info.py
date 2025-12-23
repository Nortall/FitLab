from pydantic import BaseModel, Field
from .enums import Gender, ActivityFactor
from ..value_objects.macro_distribution import MacroDistribution


class UserInfo(BaseModel):
    gender: Gender
    age: int = Field(..., ge=1, le=120)
    height_cm: float = Field(..., gt=0, le=300)
    weight_kg: float = Field(..., gt=0, le=650)
    activity_factor: ActivityFactor
    macro_distribution: MacroDistribution
