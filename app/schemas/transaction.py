from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime
from typing import Optional

class CreateTransaction(BaseModel):
    user_id: int
    amount: Decimal = Field(..., gt=0) 
    category_id: int
    type: str
    date: datetime  # yyyy-dd-mm
    description: Optional[str] = None
    

class UpdateTransaction(BaseModel):
    amount : Optional[Decimal] = None
    description : Optional[str] = None
    date : Optional[datetime] = None
