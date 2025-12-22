from sqlalchemy.orm import Session

from backend.app.nutrition.application.interfaces.db.models.nutrition_result import NutritionResultORM
from backend.app.nutrition.domain.repositories.nutrition_repository import NutritionRepository
from backend.app.nutrition.domain.entities.nutrition_result import NutritionResult
from backend.app.nutrition.domain.value_objects.macronutrients import Macronutrients


class SqlAlchemyNutritionRepository(NutritionRepository):

    def __init__(self, session: Session):
        self._session = session

    def save(self, nutrition_result: NutritionResult) -> NutritionResult:
        orm_obj = NutritionResultORM(
            #user_id=nutrition_result.user_id,
            bmr=nutrition_result.bmr,
            tdee=nutrition_result.tdee,
            protein_g=nutrition_result.macronutrients.protein_g,
            carbs_g=nutrition_result.macronutrients.carbs_g,
            fat_g=nutrition_result.macronutrients.fat_g,
        )

        self._session.add(orm_obj)
        self._session.commit()
        self._session.refresh(orm_obj)

        return NutritionResult(
            #id=orm_obj.id,
            #user_id=orm_obj.user_id,
            bmr=orm_obj.bmr,
            tdee=orm_obj.tdee,
            macronutrients=Macronutrients(
                protein_g=orm_obj.protein_g,
                carbs_g=orm_obj.carbs_g,
                fat_g=orm_obj.fat_g,
            ),
            #created_at=orm_obj.created_at,
        )

