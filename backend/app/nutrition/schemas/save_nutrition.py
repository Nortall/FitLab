from pydantic import BaseModel, Field
from typing import Optional
from .nutrition import NutritionCalculateResponse  # Используем Response схему!

class SaveNutritionRequest(BaseModel):
    """Схема запроса для сохранения УЖЕ РАССЧИТАННОГО результата"""
    calculation_result: NutritionCalculateResponse  # Готовый результат из /calculate
    name: Optional[str] = Field(None, max_length=100, description="Название расчета")

class SaveNutritionResponse(BaseModel):
    """Схема ответа при сохранении"""
    id: int
    success: bool = True
    message: str = "Calculation saved successfully"