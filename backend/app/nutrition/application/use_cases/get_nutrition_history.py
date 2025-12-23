from typing import List
from backend.app.nutrition.domain.repositories.nutrition_repository import NutritionRepository
from backend.app.nutrition.domain.entities.nutrition_result import NutritionResult


class GetNutritionHistoryUseCase:

    def __init__(self, repository: NutritionRepository):
        self._repository = repository

    def execute(self, user_id: int, limit: int, offset: int) -> List[NutritionResult]:

        return self._repository.get_history(user_id=user_id, limit=limit, offset=offset)

