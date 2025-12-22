from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.nutrition.domain.value_objects.macro_distribution import MacroDistribution
from backend.app.nutrition.schemas.nutrition_request import NutritionCalculateRequest
from backend.app.nutrition.schemas.nutrition_response import NutritionResultResponse

from backend.app.nutrition.application.use_cases.calculate_nutrition import CalculateNutritionUseCase
from backend.app.nutrition.application.interfaces.db.repositories.nutrition_repository import (
    SqlAlchemyNutritionRepository,
)
from backend.app.nutrition.domain.services.nutrition_calculator import NutritionCalculator
from backend.app.nutrition.domain.entities.user_info import UserInfo

router = APIRouter(prefix="/nutrition", tags=["Nutrition"])


@router.post("/calculate", response_model=NutritionResultResponse)
def calculate_nutrition(
    request: NutritionCalculateRequest,
):
    user_info = UserInfo(
        gender=request.gender,
        age=request.age,
        height_cm=request.height_cm,
        weight_kg=request.weight_kg,
        activity_factor=request.activity_factor,
        macro_distribution=MacroDistribution(
            protein_pct=request.macro_distribution.protein_pct,
            carbs_pct=request.macro_distribution.carbs_pct,
            fat_pct=request.macro_distribution.fat_pct,
        )
    )

    use_case = CalculateNutritionUseCase(
        calculator=NutritionCalculator()
    )

    return use_case.execute(user_info)

