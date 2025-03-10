from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.auth.oauth2 import get_current_user
from app.schemas.transaction import CreateTransaction, UpdateTransaction
from app.database import get_db
from app.models import Transaction, Category, User
from app.utils.logger import Logger

router  = APIRouter()
logging = Logger.get_instance()


@router.post("/", status_code=status.HTTP_201_CREATED)
def transaction(transaction: CreateTransaction, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if transaction.category_id:
        category = db.query(Category).filter(
            Category.id == transaction.category_id,
            (Category.user_id == current_user.id) | (Category.is_default == True)  # Allow both user and default categories
        ).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with ID {transaction.category_id} not found.",
            )

    new_transaction = Transaction(
        amount=transaction.amount,
        description=transaction.description,
        category_id=transaction.category_id,
        type=transaction.type,
        user_id=current_user.id,
        date=transaction.date if transaction.date else None,
    )
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    logging.info(f"Transaction created: user_id={new_transaction.user_id}, transaction_id={new_transaction.id}")

    return {
        "user_id": new_transaction.user_id,
        "id": new_transaction.id
    }


@router.get("/")
def get_transaction(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    transactions = db.query(Transaction).filter(Transaction.user_id==current_user.id).all()
    logging.info(f"Fetched transactions for user_id={current_user.id}")
    return transactions


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(transaction_id, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    transaction_query = db.query(Transaction).filter(transaction_id==Transaction.id)
    transaction = transaction_query.first()

    if transaction==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"transaction with ID {transaction_id} not found")
    
    if current_user.id!=transaction.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized")
    
    transaction_query.delete(synchronize_session=False)
    db.commit()
    logging.info(f"Transaction deleted: user_id={current_user.id}, transaction_id={transaction_id}")


@router.put("/{transaction_id}")
def update_transaction(transaction_id, transaction: UpdateTransaction ,db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    transaction_query = db.query(Transaction).filter(transaction_id==Transaction.id)
    transaction_found = transaction_query.first()

    if not transaction_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"transaction with ID {transaction_id} not found")
    
    if current_user.id!=transaction_found.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized")
    
    update_data = transaction.dict(exclude_unset=True)
    
    transaction_query.update(values=update_data, synchronize_session=False)
    db.commit()
    logging.info(f"Transaction updated: user_id={current_user.id}, transaction_id={transaction_id}, updates={update_data}")

    return {
        "message": "transaction updated"
    }
    

