from __future__ import annotations
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from ..value_objects.macronutrients import Macronutrients


class NutritionResult(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    bmr: float
    tdee: float
    macronutrients: Macronutrients
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True


class UpdateNutritionResult(BaseModel):
    bmr: Optional[float] = Field(None, gt=0)
    tdee: Optional[float] = Field(None, gt=0)
    macronutrients: Optional[Macronutrients] = None

    class Config:
        from_attributes = True


