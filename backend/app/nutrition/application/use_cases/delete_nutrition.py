from backend.app.nutrition.domain.repositories.nutrition_repository import NutritionRepository


class DeleteNutritionUseCase:
    def __init__(self, repository: NutritionRepository):
        self._repository = repository

    def execute(self, calculation_id: int, user_id: int) -> bool:
        """
        Удаляет расчет питания

        Args:
            calculation_id: ID расчета
            user_id: ID пользователя (для проверки владельца)

        Returns:
            bool: True если удалено, False если не найдено
        """
        return self._repository.delete(calculation_id, user_id)