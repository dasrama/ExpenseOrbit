from pydantic import BaseModel
from datetime import date

class CreateSavingsGoal(BaseModel):
    name: str
    target_amount: float
    target_date: date

class SavingsGoalResponse(BaseModel):
    id: int
    name: str
    target_amount: float
    target_date: date
    is_completed: bool
    progress: float = 0.0  # Progress as a percentage of target

    class Config:
        orm_mode = True
