from typing import List
from pydantic import BaseModel
from backend.app.nutrition.domain.value_objects.macronutrients import Macronutrients
from datetime import datetime


class NutritionHistoryItem(BaseModel):
    id: int
    bmr: float
    tdee: float
    macronutrients: Macronutrients
    created_at: datetime


class NutritionHistoryResponse(BaseModel):
    items: List[NutritionHistoryItem]
    count: int
