from __future__ import annotations

from backend.app.nutrition.domain.repositories.nutrition_repository import NutritionRepository
from backend.app.nutrition.domain.entities.nutrition_result import NutritionResult
from backend.app.nutrition.domain.entities.user_info import UserInfo
from backend.app.nutrition.domain.services.nutrition_calculator import NutritionCalculator


class CalculateNutritionUseCase:

    def __init__(self, calculator: NutritionCalculator):
        self._calculator = calculator

    def execute(self, user_info: UserInfo) -> NutritionResult:
        # 1. Расчёт питания
        nutrition_result = self._calculator.calculate(user_info)

        result_with_user = NutritionResult(bmr=nutrition_result.bmr, tdee=nutrition_result.tdee, macronutrients=nutrition_result.macronutrients)

        # 2. Возврат результата
        return result_with_user

