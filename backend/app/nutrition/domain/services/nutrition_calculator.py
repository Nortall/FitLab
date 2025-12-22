from backend.app.nutrition.domain.entities.nutrition_result import NutritionResult
from backend.app.nutrition.domain.entities.user_info import UserInfo
from backend.app.nutrition.domain.value_objects.macronutrients import Macronutrients

class NutritionCalculator:
    """
        Domain service responsible for calculating daily nutrition needs.
    """
    def calculate(self, user: UserInfo) -> NutritionResult:
        bmr = self._calculate_bmr_Harrison_Benedict(user)
        tdee = bmr * user.activity_factor.value

        macronutrients = self._calculate_macronutrients(calories=tdee, distribution=user.macro_distribution)

        return NutritionResult(bmr=round(bmr, 2), tdee=round(tdee, 2), macronutrients=macronutrients)

    def _calculate_bmr_Harrison_Benedict(self, user: UserInfo) -> float:
        if user.gender == user.gender.MALE:
            return 88.36 + (13.4 * user.weight_kg) + (4.8 * user.height_cm) - (5.7 * user.age)
        else:
            return 447.6 + (9.2 * user.weight_kg) + (3.1 * user.height_cm) - (4.3 * user.age)

    def _calculate_tdee(self, bmr: float, activity_factor: float) -> float:
        return bmr * activity_factor

    def _calculate_macronutrients(self, calories: float, distribution) -> Macronutrients:
        protein_cal = calories * distribution.protein_pct / 100
        carbs_cal = calories * distribution.carbs_pct / 100
        fat_cal = calories * distribution.fat_pct / 100

        return Macronutrients(protein_g=protein_cal / 4, carbs_g=carbs_cal / 4, fat_g=fat_cal / 9)






