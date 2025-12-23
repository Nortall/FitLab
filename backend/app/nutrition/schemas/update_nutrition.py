from typing import Optional
from pydantic import BaseModel, Field
from backend.app.nutrition.domain.value_objects.macronutrients import Macronutrients


class UpdateNutritionRequest(BaseModel):
    """Схема запроса для обновления расчета"""
    bmr: Optional[float] = Field(None, gt=0, description="Базальный метаболизм")
    tdee: Optional[float] = Field(None, gt=0, description="Суточный расход калорий")
    macronutrients: Optional[Macronutrients] = Field(
        None,
        description="Макронутриенты (белки, жиры, углеводы)"
    )

    class Config:
        from_attributes = True


class UpdateNutritionResponse(BaseModel):
    """Схема ответа при обновлении"""
    id: int
    success: bool = True
    message: str = "Calculation updated successfully"


class DeleteNutritionResponse(BaseModel):
    """Схема ответа при удалении"""
    success: bool
    message: str


class NutritionDetailResponse(BaseModel):
    """Схема ответа для деталей расчета"""
    id: int
    bmr: float
    tdee: float
    macronutrients: Macronutrients
    created_at: str

    class Config:
        from_attributes = True