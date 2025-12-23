from abc import ABC, abstractmethod
from typing import List, Optional

from backend.app.nutrition.domain.entities.nutrition_result import NutritionResult, UpdateNutritionResult


class NutritionRepository(ABC):

    @abstractmethod
    def save(self, nutrition_result: NutritionResult) -> NutritionResult:
        pass

    @abstractmethod
    def get_history(self, user_id: int, limit: int, offset: int) -> List[NutritionResult]:
        pass

    @abstractmethod
    def update(self, calculation_id: int, user_id: int, update_data: UpdateNutritionResult) -> Optional[NutritionResult]:
        pass

    @abstractmethod
    def delete(self, calculation_id: int, user_id: int) -> bool:
        pass

    @abstractmethod
    def get_by_id(self, calculation_id: int, user_id: int) -> Optional[NutritionResult]:
        pass

