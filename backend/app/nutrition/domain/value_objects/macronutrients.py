from pydantic import BaseModel, field_validator, Field

class Macronutrients(BaseModel):
    protein_g: float = Field(..., ge=0)
    carbs_g: float = Field(..., ge=0)
    fat_g: float = Field(..., ge=0)


    def calories(self) -> float:
        return self.protein_g * 4 + self.carbs_g * 4 + self.fat_g * 4