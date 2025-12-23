from typing import Optional
from backend.app.nutrition.domain.repositories.nutrition_repository import NutritionRepository
from backend.app.nutrition.domain.entities.nutrition_result import (
    NutritionResult,
    UpdateNutritionResult
)


class UpdateNutritionUseCase:
    def __init__(self, repository: NutritionRepository):
        self._repository = repository

    def execute(self, calculation_id: int, user_id: int, update_data: UpdateNutritionResult) -> Optional[NutritionResult]:
        """
        Обновляет расчет питания

        Args:
            calculation_id: ID расчета
            user_id: ID пользователя (для проверки владельца)
            update_data: Данные для обновления

        Returns:
            Optional[NutritionResult]: Обновленный расчет или None если не найден
        """
        return self._repository.update(calculation_id, user_id, update_data)