from sqlalchemy import Column, Integer, String, Boolean, ForeignKey 
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

from app.database import Base 


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable= False, unique=True )    
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

    """ to define rollback condition if user enters invalid content to further prevent the count of id to original one"""

class Transaction(Base):
    __tablename__ = "transactions"

    id=Column(Integer, nullable=False, primary_key=True)
    description=Column(String, nullable=False, unique=True)
    amount=Column(Integer, nullable=False)
    date=Column(TIMESTAMP, nullable=False)
    category=Column(String, nullable=False)
    user_id=Column(Integer, nullable=False)


