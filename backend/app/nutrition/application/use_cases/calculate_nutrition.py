from __future__ import annotations

from backend.app.nutrition.domain.repositories.nutrition_repository import NutritionRepository
from backend.app.nutrition.domain.entities.nutrition_result import NutritionResult
from backend.app.nutrition.domain.entities.user_info import UserInfo
from backend.app.nutrition.domain.services.nutrition_calculator import NutritionCalculator


class CalculateNutritionUseCase:

    def __init__(self, calculator: NutritionCalculator):
        self._calculator = calculator
        #self._repository = repository

    def execute(self, user_info: UserInfo) -> NutritionResult:
        # 1. Расчёт питания
        nutrition_result = self._calculator.calculate(user_info)

        # 2. Сохранение результата
        #saved_result = self._repository.save(nutrition_result)

        # 3. Возврат результата
        return nutrition_result

