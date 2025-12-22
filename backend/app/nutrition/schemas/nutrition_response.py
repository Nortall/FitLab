from datetime import datetime
from pydantic import BaseModel, Field
from backend.app.nutrition.domain.value_objects.macronutrients import Macronutrients


class NutritionResultResponse(BaseModel):
    #id: int = Field(..., description="Unique Nutrition Result identifier")
    #user_id: int
    bmr: float
    tdee: float
    macronutrients: Macronutrients
    #created_at: datetime

    class Config:
        form_attributes = True

