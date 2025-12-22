from datetime import datetime
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from backend.app.database import Base

class NutritionResultORM(Base):
    __tablename__ = "nutrition_results"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)

    bmr = Column(Float, nullable=False)
    tdee = Column(Float, nullable=False)

    protein_g = Column(Float, nullable=False)
    carbs_g = Column(Float, nullable=False)
    fat_g = Column(Float, nullable=False)

    #created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"NutritionResultORM(id={self.id}, user_id={self.user_id})"
