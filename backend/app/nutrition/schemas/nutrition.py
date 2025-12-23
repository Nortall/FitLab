from datetime import datetime
from pydantic import BaseModel, Field
from backend.app.nutrition.domain.entities.enums import Gender, ActivityFactor
from backend.app.nutrition.domain.value_objects.macro_distribution import MacroDistribution
from backend.app.nutrition.domain.value_objects.macronutrients import Macronutrients


class NutritionBase(BaseModel):
    gender: Gender
    age: int = Field(..., ge=0, le=100)
    height_cm: float = Field(..., ge=0, le=300)
    weight_kg: float = Field(..., ge=0, le=650)

    activity_factor: ActivityFactor
    macro_distribution: MacroDistribution

class NutritionCalculateRequest(NutritionBase):
    pass


class NutritionCalculateResponse(BaseModel):
        bmr: float
        tdee: float
        macronutrients: Macronutrients
        created_at: datetime
