from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, Date, Enum, BigInteger, CheckConstraint
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import Session, relationship
from enum import Enum as pyEnum

from app.database import Base 
from app.schemas.category import DefaultCategory 


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    discord_id = Column(BigInteger, unique=True, nullable=True)
    email = Column(String, unique=True)    
    password = Column(String)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    categories = relationship("Category", back_populates="user", cascade="all, delete-orphan")
    savings = relationship("SavingsGoal", back_populates="user", cascade="all, delete-orphan") 

    __table_args__ = (
        CheckConstraint(
            "(discord_id IS NOT NULL AND email IS NULL AND password IS NULL) OR "
            "(discord_id IS NULL AND email IS NOT NULL AND password IS NOT NULL)",
            name="check_user_authentication"
        ),
    )

    """ to define rollback condition if user enters invalid content to further prevent the count of id to original one"""

class TransactionType(pyEnum):
    INCOME="income"
    SAVINGS="savings"
    EXPENSE="expense"

class Transaction(Base):
    __tablename__ = "transactions"

    id=Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    description=Column(String, nullable=False, unique=True)
    amount=Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    date=Column(TIMESTAMP, nullable=False)
    
    category = relationship("Category")
    user = relationship("User")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)  # Nullable for default categories
    is_default = Column(Boolean, default=False)  # Flag to indicate if a category is default

    user = relationship("User", back_populates="categories")


class SavingsGoal(Base):
    __tablename__ = "savings"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    target_amount = Column(Float, nullable=False)
    saved_amount = Column(Float, default=0.0) 
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    target_date = Column(Date, nullable=True) 

    user = relationship("User", back_populates="savings")


def seed_default_categories(db: Session):
    for category in DefaultCategory:
        existing_category = db.query(Category).filter(Category.name == category.value, Category.is_default == True).first()
        if not existing_category:
            new_category = Category(name=category.value, is_default=True)
            db.add(new_category)
    db.commit()    



