from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import func
from typing import List

from app.database import get_db
from app.auth.oauth2 import get_current_user
from app.models import SavingsGoal, Transaction, User, Category
from app.schemas.savings import CreateSavingsGoal, SavingsGoalResponse, UpdateSavingsGoal

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_savings_goal(goal: CreateSavingsGoal, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_goal = SavingsGoal(
        name=goal.name,
        target_amount=goal.target_amount,
        user_id=current_user.id,
        target_date=goal.target_date
    )
    db.add(new_goal)
    db.commit()
    db.refresh(new_goal)
    return {
        "id": new_goal.id,
        "name": new_goal.name,
        "target_amount": new_goal.target_amount
    }


@router.get("/", response_model=List[SavingsGoalResponse])
def get_savings_goals(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    goals = db.query(SavingsGoal).filter(SavingsGoal.user_id == current_user.id).all()
    return goals


@router.put("/{goal_id}")
def update_savings_goal(goal_id: int, updated_goal: UpdateSavingsGoal, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    goal_query = db.query(SavingsGoal).filter(SavingsGoal.id == goal_id, SavingsGoal.user_id == current_user.id)
    goal = goal_query.first()

    if not goal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Savings goal with ID {goal_id} not found.")

    goal_query.update(updated_goal.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return {"message": "Savings goal updated."}


@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_savings_goal(goal_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    goal_query = db.query(SavingsGoal).filter(SavingsGoal.id == goal_id, SavingsGoal.user_id == current_user.id)
    goal = goal_query.first()

    if not goal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Savings goal with ID {goal_id} not found.")

    goal_query.delete(synchronize_session=False)
    db.commit()


@router.get("/progress/{goal_id}")
def get_saving_progress(goal_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    goal = db.query(SavingsGoal).filter(SavingsGoal.id == goal_id, SavingsGoal.user_id == current_user.id).first()

    if not goal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Savings goal with ID {goal_id} not found.")

    total_saved = db.query(func.sum(Transaction.amount)).join(Category).filter(
        Transaction.user_id == current_user.id,
        Category.name == "Savings"
    ).scalar() or 0 

    progress = (total_saved / goal.target_amount) * 100 if goal.target_amount else 0


    return {
        "goal_name": goal.name,
        "target_amount": goal.target_amount,
        "saved_amount": total_saved,
        "progress_percentage": progress,
        "remaining_amount": max(0, goal.target_amount - total_saved)
    }
