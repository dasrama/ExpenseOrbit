"""from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import Settings


settings = Settings()

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import Settings

class Database:
    def __init__(self):
        self.settings = Settings()
        self.SQLALCHEMY_DATABASE_URL = f'postgresql://{self.settings.DATABASE_USERNAME}:' \
                                       f'{self.settings.DATABASE_PASSWORD}@{self.settings.DATABASE_HOST}:' \
                                       f'{self.settings.DATABASE_PORT}/{self.settings.DATABASE_NAME}'

        self.engine = create_engine(self.SQLALCHEMY_DATABASE_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.Base = declarative_base()

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

# Initialize the Database class instance
database = Database()

# Now, `database.engine`, `database.Base`, and `database.get_db()` can be imported and used in other parts of your project.
