from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from app.database import get_db
from app.models import SavingsGoal, Transaction
from app.schemas.savings import CreateSavingsGoal, SavingsGoalResponse

router = APIRouter()

@router.post("/", response_model=SavingsGoalResponse)
def create_savings_goal(goal: CreateSavingsGoal, db: Session = Depends(get_db), user_id: int = 1):
    new_goal = SavingsGoal(
        user_id=user_id,
        name=goal.name,
        target_amount=goal.target_amount,
        target_date=goal.target_date,
    )
    db.add(new_goal)
    db.commit()
    db.refresh(new_goal)
    return new_goal


@router.get("/", response_model=List[SavingsGoalResponse])
def get_savings_goals(db: Session = Depends(get_db), user_id: int = 1):
    goals = db.query(SavingsGoal).filter(SavingsGoal.user_id == user_id).all()
    for goal in goals:
        total_saved = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.category == "Savings",
            Transaction.date <= goal.target_date
        ).scalar() or 0
        goal.progress = min(total_saved / goal.target_amount, 1.0)
    return goals



@router.put("/{goal_id}/complete", response_model=SavingsGoalResponse)
def complete_savings_goal(goal_id: int, db: Session = Depends(get_db), user_id: int = 1):
    goal = db.query(SavingsGoal).filter(SavingsGoal.id == goal_id, SavingsGoal.user_id == user_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Savings goal not found")
    
    goal.is_completed = True
    db.commit()
    db.refresh(goal)
    return goal
