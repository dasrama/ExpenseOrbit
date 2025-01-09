from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Category
from app.schemas.category import CategoryCreate, CategoryResponse

router = APIRouter()


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate, db: Session = Depends(get_db), user_id: int = 1):  # Replace with real user_id
    existing_category = db.query(Category).filter(Category.name == category.name, Category.user_id == user_id).first()
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category already exists.",
        )

    new_category = Category(name=category.name, user_id=user_id)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


@router.get("/", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db), user_id: int = 1):  # Replace with real user_id
    categories = db.query(Category).filter(Category.user_id == user_id).all()
    return categories


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db), user_id: int = 1):  # Replace with real user_id
    category = db.query(Category).filter(Category.id == category_id, Category.user_id == user_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with ID {category_id} not found.",
        )

    db.delete(category)
    db.commit()
