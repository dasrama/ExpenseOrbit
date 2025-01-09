from enum import Enum
from pydantic import BaseModel
from typing import Optional

class DefaultCategory(Enum):
    FOOD = "Food"
    RENT = "Rent"
    ENTERTAINMENT = "Entertainment"
    GROCERIES = "Groceries"
    TRANSPORT = "Transport"


class CategoryCreate(BaseModel):
    name: str

class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

