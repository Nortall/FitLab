from backend.app.nutrition.domain.repositories.nutrition_repository import NutritionRepository
from backend.app.nutrition.domain.entities.nutrition_result import NutritionResult


class SaveNutritionUseCase:
    def __init__(self, repository: NutritionRepository):
        self.repository = repository

    def execute(self, result: NutritionResult) -> NutritionResult:
        """
        Сохраняет результат расчета питания

        Args:
            user_id: ID пользователя
            nutrition_result: Результат расчета

        Returns:
            int: ID сохраненной записи в БД
            :param result:
        """
        return self.repository.save(result)