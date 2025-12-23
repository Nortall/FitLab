from typing import Optional
from datetime import datetime
from backend.app.nutrition.application.interfaces.db.models.nutrition_result import NutritionResultORM
from backend.app.nutrition.domain.entities.nutrition_result import NutritionResult
from backend.app.nutrition.domain.value_objects.macronutrients import Macronutrients


class NutritionMapper:
    """Преобразует между ORM и Domain объектами"""

    @staticmethod
    def to_domain(orm_obj: NutritionResultORM) -> NutritionResult:
        """ORM -> Domain"""
        if not orm_obj:
            return None

        return NutritionResult(
            id=orm_obj.id,
            user_id=orm_obj.user_id,
            bmr=orm_obj.bmr,
            tdee=orm_obj.tdee,
            macronutrients=Macronutrients(
                protein_g=orm_obj.protein_g,
                carbs_g=orm_obj.carbs_g,
                fat_g=orm_obj.fat_g,
            ),
            created_at=orm_obj.created_at,
        )

    @staticmethod
    def to_orm(domain_obj: NutritionResult) -> NutritionResultORM:
        """Domain -> ORM (для создания)"""
        return NutritionResultORM(
            id=domain_obj.id if domain_obj.id else None,
            user_id=domain_obj.user_id,
            bmr=domain_obj.bmr,
            tdee=domain_obj.tdee,
            protein_g=domain_obj.macronutrients.protein_g,
            carbs_g=domain_obj.macronutrients.carbs_g,
            fat_g=domain_obj.macronutrients.fat_g,
            created_at=domain_obj.created_at or datetime.utcnow(),
        )