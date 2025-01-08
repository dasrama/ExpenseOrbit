from sqlalchemy import Column, Integer, String, Boolean, ForeignKey 
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.ext.declarative import declarative_base

from app.database import database

Base = declarative_base()

class User(database.Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable= False, unique=True )    
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

    """ to define rollback condition if user enters invalid content to further prevent the count of id to original one"""