from abc import ABC, abstractmethod
from backend.app.nutrition.domain.entities.nutrition_result import NutritionResult


class NutritionRepository(ABC):

    @abstractmethod
    def save(self, nutrition_result: NutritionResult) -> NutritionResult:
        pass