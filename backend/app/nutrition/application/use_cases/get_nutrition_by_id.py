from typing import Optional
from backend.app.nutrition.domain.repositories.nutrition_repository import NutritionRepository
from backend.app.nutrition.domain.entities.nutrition_result import NutritionResult


class GetNutritionByIdUseCase:
    def __init__(self, repository: NutritionRepository):
        self._repository = repository

    def execute(self, calculation_id: int, user_id: int) -> Optional[NutritionResult]:
        """
        Получает расчет по ID

        Args:
            calculation_id: ID расчета
            user_id: ID пользователя (для проверки владельца)

        Returns:
            Optional[NutritionResult]: Расчет или None если не найден
        """
        return self._repository.get_by_id(calculation_id, user_id)