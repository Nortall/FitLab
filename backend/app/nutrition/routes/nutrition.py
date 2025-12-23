from fastapi import APIRouter, Depends, Query, HTTPException, Path
from sqlalchemy.orm import Session
from starlette import status
from backend.app.auth.dependencies import get_current_user_id
from backend.app.database import get_db
from backend.app.nutrition.application.interfaces.db.models.nutrition_result import NutritionResultORM
from backend.app.nutrition.application.interfaces.db.repositories.nutrition_repository import \
    SqlAlchemyNutritionRepository
from backend.app.nutrition.application.use_cases.delete_nutrition import DeleteNutritionUseCase
from backend.app.nutrition.application.use_cases.get_nutrition_by_id import GetNutritionByIdUseCase
from backend.app.nutrition.application.use_cases.get_nutrition_history import GetNutritionHistoryUseCase
from backend.app.nutrition.application.use_cases.save_nutrition import SaveNutritionUseCase
from backend.app.nutrition.application.use_cases.update_nutrition import UpdateNutritionUseCase
from backend.app.nutrition.domain.entities.nutrition_result import NutritionResult, UpdateNutritionResult
from backend.app.nutrition.domain.value_objects.macro_distribution import MacroDistribution
from backend.app.nutrition.domain.value_objects.macronutrients import Macronutrients
from backend.app.nutrition.schemas.history import NutritionHistoryResponse, NutritionHistoryItem
from backend.app.nutrition.schemas.nutrition import NutritionCalculateRequest
from backend.app.nutrition.schemas.nutrition import NutritionCalculateResponse

from backend.app.nutrition.application.use_cases.calculate_nutrition import CalculateNutritionUseCase
from backend.app.nutrition.domain.services.nutrition_calculator import NutritionCalculator
from backend.app.nutrition.domain.entities.user_info import UserInfo
from backend.app.nutrition.schemas.save_nutrition import SaveNutritionResponse, SaveNutritionRequest
from backend.app.nutrition.schemas.update_nutrition import DeleteNutritionResponse, UpdateNutritionResponse, \
    UpdateNutritionRequest, NutritionDetailResponse

router = APIRouter(prefix="/nutrition", tags=["Nutrition"])


@router.post("/calculate", response_model=NutritionCalculateResponse)
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
        calculator=NutritionCalculator(),
    )

    return use_case.execute(user_info=user_info)



@router.post("/save", response_model=SaveNutritionResponse, status_code=status.HTTP_201_CREATED)
def save_nutrition(
    request: SaveNutritionRequest,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    calc = request.calculation_result

    domain_result = NutritionResult(
        user_id=user_id,
        bmr=calc.bmr,
        tdee=calc.tdee,
        macronutrients=calc.macronutrients,
    )

    repository = SqlAlchemyNutritionRepository(db)
    use_case = SaveNutritionUseCase(repository)

    saved = use_case.execute(domain_result)

    return SaveNutritionResponse(
        id=saved.id,
        message=f"Saved with ID: {saved.id}"
    )


@router.get("/history", response_model=NutritionHistoryResponse)
def get_nutrition_history(
        user_id: int = Depends(get_current_user_id),
        db: Session = Depends(get_db),
        limit: int = Query(10, ge=1, le=100),
        offset: int = Query(0, ge=0),
):
    repository = SqlAlchemyNutritionRepository(db)
    use_case = GetNutritionHistoryUseCase(repository)

    # Получаем историю
    results = use_case.execute(user_id, limit, offset)

    # Преобразуем в схему
    history_items = [
        NutritionHistoryItem(
            id=result.id,
            bmr=result.bmr,
            tdee=result.tdee,
            macronutrients=result.macronutrients,
            created_at=result.created_at,
        )
        for result in results  # Теперь result точно NutritionResult
    ]

    return NutritionHistoryResponse(
        items=history_items,
        count=len(history_items),
    )


@router.get("/{calculation_id}", response_model=NutritionDetailResponse)
def get_nutrition_by_id(
        calculation_id: int = Path(..., ge=1, description="ID расчета"),
        user_id: int = Depends(get_current_user_id),
        db: Session = Depends(get_db),
):
    """Получает конкретный расчет по ID"""
    repository = SqlAlchemyNutritionRepository(db)
    use_case = GetNutritionByIdUseCase(repository)

    result = use_case.execute(calculation_id, user_id)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found or access denied"
        )

    return NutritionDetailResponse(
        id=result.id,
        bmr=result.bmr,
        tdee=result.tdee,
        macronutrients=result.macronutrients,
        created_at=result.created_at.isoformat() if result.created_at else None,
    )


@router.put("/{calculation_id}", response_model=UpdateNutritionResponse)
def update_nutrition(
        calculation_id: int = Path(..., ge=1, description="ID расчета"),
        update_data: UpdateNutritionRequest = ...,
        user_id: int = Depends(get_current_user_id),
        db: Session = Depends(get_db),
):
    """Обновляет существующий расчет"""
    repository = SqlAlchemyNutritionRepository(db)
    use_case = UpdateNutritionUseCase(repository)

    # Преобразуем схему запроса в доменную модель
    domain_update_data = UpdateNutritionResult(
        bmr=update_data.bmr,
        tdee=update_data.tdee,
        macronutrients=update_data.macronutrients,
    )

    updated_result = use_case.execute(calculation_id, user_id, domain_update_data)

    if not updated_result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found or access denied"
        )

    return UpdateNutritionResponse(
        id=updated_result.id,
        message=f"Calculation {calculation_id} updated successfully"
    )


@router.delete("/{calculation_id}", response_model=DeleteNutritionResponse)
def delete_nutrition(
        calculation_id: int = Path(..., ge=1, description="ID расчета"),
        user_id: int = Depends(get_current_user_id),
        db: Session = Depends(get_db),
):
    """Удаляет расчет"""
    repository = SqlAlchemyNutritionRepository(db)
    use_case = DeleteNutritionUseCase(repository)

    success = use_case.execute(calculation_id, user_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found or access denied"
        )

    return DeleteNutritionResponse(
        success=True,
        message=f"Calculation {calculation_id} deleted successfully"
    )


@router.get("/debug/all")
def debug_all(db: Session = Depends(get_db)):
    return db.query(NutritionResultORM).all()


