from datetime import datetime
from typing import List, Optional

from sqlalchemy import desc, and_
from sqlalchemy.orm import Session

from backend.app.nutrition.application.interfaces.db.mappers.nutrition_mapper import NutritionMapper
from backend.app.nutrition.application.interfaces.db.models.nutrition_result import NutritionResultORM
from backend.app.nutrition.domain.repositories.nutrition_repository import NutritionRepository
from backend.app.nutrition.domain.entities.nutrition_result import NutritionResult, UpdateNutritionResult
from backend.app.nutrition.domain.value_objects.macronutrients import Macronutrients


class SqlAlchemyNutritionRepository(NutritionRepository):

    def __init__(self, session: Session):
        self._session = session

    def save(self, nutrition_result: NutritionResult) ->  NutritionResult:
        orm_obj = NutritionResultORM(
            user_id=nutrition_result.user_id,
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
            id=orm_obj.id,
            user_id=orm_obj.user_id,
            bmr=orm_obj.bmr,
            tdee=orm_obj.tdee,
            macronutrients=nutrition_result.macronutrients,
            created_at=orm_obj.created_at,
        )

    def get_history(self, user_id: int, limit: int = 10, offset: int = 0) -> List[NutritionResult]:

        orm_results = (self._session.query(NutritionResultORM).filter(NutritionResultORM.user_id == user_id).order_by(desc(NutritionResultORM.created_at)).limit(limit).offset(offset).all())

        return [
            NutritionResult(
                id=row.id,
                user_id=row.user_id,
                bmr=row.bmr,
                tdee=row.tdee,
                macronutrients=Macronutrients(
                    protein_g=row.protein_g,
                    carbs_g=row.carbs_g,
                    fat_g=row.fat_g,
                ),
                created_at=row.created_at,
            )
            for row in orm_results
        ]

    def get_by_id(self, calculation_id: int, user_id: int) -> Optional[NutritionResult]:

        orm_obj = (self._session.query(NutritionResultORM).filter(and_(NutritionResultORM.id == calculation_id, NutritionResultORM.user_id == user_id)).first())

        if not orm_obj:
            return None

        return NutritionMapper.to_domain(orm_obj)

    def update(self, calculation_id: int, user_id: int, update_data: UpdateNutritionResult) -> Optional[NutritionResult]:
        """Обновляет существующий расчет"""

        orm_obj = (self._session.query(NutritionResultORM).filter(and_(NutritionResultORM.id == calculation_id, NutritionResultORM.user_id == user_id)).first())

        if not orm_obj:
            return None

        # Обновляем поля если они переданы
        if update_data.bmr is not None:
            orm_obj.bmr = update_data.bmr

        if update_data.tdee is not None:
            orm_obj.tdee = update_data.tdee

        if update_data.macronutrients is not None:
            orm_obj.protein_g = update_data.macronutrients.protein_g
            orm_obj.carbs_g = update_data.macronutrients.carbs_g
            orm_obj.fat_g = update_data.macronutrients.fat_g

        self._session.commit()
        self._session.refresh(orm_obj)

        return NutritionMapper.to_domain(orm_obj)

    def delete(self, calculation_id: int, user_id: int) -> bool:

        orm_obj = (self._session.query(NutritionResultORM).filter(and_(NutritionResultORM.id == calculation_id, NutritionResultORM.user_id == user_id)).first())

        if not orm_obj:
            return False

        # Удаляем
        self._session.delete(orm_obj)
        self._session.commit()

        return True






