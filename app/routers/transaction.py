from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.schemas.transaction import CreateTransaction, UpdateTransaction
from app.database import get_db
from app.models import Transaction

router  = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
def transaction(transaction: CreateTransaction, db: Session = Depends(get_db)):
    new_transaction=Transaction(**transaction.dict())
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return {
        "user_id": transaction.user_id,
        "id": transaction.id
    }


@router.get("/{transaction_id}")
def get_transaction(transaction_id, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(transaction_id==Transaction.id).first()
    return transaction


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(transaction_id, db: Session = Depends(get_db)):
    transaction_query = db.query(Transaction).filter(transaction_id==Transaction.id)
    transaction = transaction_query.first()
    print(transaction)

    if transaction==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="transaction with {transaction_id} not found")

    transaction_query.delete(synchronize_session=False)
    db.commit()


@router.put("/{transaction_id}")
def update_transaction(transaction_id, transaction: UpdateTransaction ,db: Session = Depends(get_db)):
    transaction_query = db.query(Transaction).filter(transaction_id==Transaction.id)
    transaction_found = transaction_query.first()
    print(transaction)

    if not transaction_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="transaction with id: {transaction_id} not found")
    
    update_data = transaction.dict(exclude_unset=True)
    
    transaction_query.update(values=update_data, synchronize_session=False)
    db.commit()

    return {
        "message": "transaction updated"
    }
    

