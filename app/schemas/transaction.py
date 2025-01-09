from pydantic import BaseModel, Field, validator
from decimal import Decimal
from datetime import datetime
from typing import Optional

class CreateTransaction(BaseModel):
    user_id: int
    amount: Decimal = Field(..., gt=0) 
    category_id: int
    date: datetime 
    description: Optional[str] = None

    @validator("date", pre=True)
    def parse_date(cls, value):
        """Validator to handle custom date formats like 'DD-MM-YYYY'."""
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%d-%m-%Y")
            except ValueError:
                raise ValueError("Date must be in the format DD-MM-YYYY.")
        return value
    

class UpdateTransaction(BaseModel):
    amount : Optional[Decimal] = None
    description : Optional[str] = None
    date : Optional[datetime] = None
