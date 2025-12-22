from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, Field
from ..value_objects.macronutrients import Macronutrients


class NutritionResult(BaseModel):
    #id: int
    #user_id: int
    bmr: float
    tdee: float
    macronutrients: Macronutrients
    #created_at: datetime = Field(default_factory=datetime.utcnow)
