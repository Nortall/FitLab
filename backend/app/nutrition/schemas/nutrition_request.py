from pydantic import BaseModel, Field
from backend.app.nutrition.domain.entities.enums import Gender, ActivityFactor
from backend.app.nutrition.domain.value_objects.macro_distribution import MacroDistribution


class NutritionCalculateRequest(BaseModel):
    #user_id: int = Field(..., description="Unique User identifier")

    gender: Gender
    age: int = Field(..., ge=0, le=100)
    height_cm: float = Field(..., ge=0, le=300)
    weight_kg: float = Field(..., ge=0, le=650)

    activity_factor: ActivityFactor
    macro_distribution: MacroDistribution

    class Config:
        form_attributes = True


