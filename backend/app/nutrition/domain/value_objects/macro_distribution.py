from pydantic import BaseModel, Field, model_validator


class MacroDistribution(BaseModel):
    protein_pct: int = Field(..., ge=0, le=100)
    carbs_pct: int = Field(..., ge=0, le=100)
    fat_pct: int = Field(..., ge=0, le=100)

    @model_validator(mode="after")
    def validate_total(self):
        total = self.protein_pct + self.carbs_pct + self.fat_pct
        if total != 100:
            raise ValueError("Total macro percentage must be equal to 100")
        return self
