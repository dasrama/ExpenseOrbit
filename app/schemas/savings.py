from pydantic import BaseModel
from datetime import date
from typing import Optional

class CreateSavingsGoal(BaseModel):
    name: str
    target_amount: float
    target_date: date

class UpdateSavingsGoal(BaseModel):
    name: Optional[str] = None
    target_amount: Optional[float] = None
    target_date: Optional[date] = None

class SavingsGoalResponse(BaseModel):
    id: int
    name: str
    target_amount: float
    target_date: date

    class Config:
        orm_mode = True
