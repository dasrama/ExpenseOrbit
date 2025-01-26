from fastapi import FastAPI
from sqlalchemy.orm import Session

from app import models
from app.database import engine
from app.models import seed_default_categories
from app.routers.auth import router as AuthBackend
from app.routers.user import router as UserRouter
from app.routers.transaction import router as TransactionRouter
from app.routers.category import router as CategoryRouter
from app.routers.savings import router as SavingsRouter
from app.routers.report import router as ReportRouter
from app.utils.logger import Logger


# will create all the corresponding tables in the database based on models defined in model.py .
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()
logging = Logger.get_instance()


@app.on_event("startup")
def on_startup():
    logging.info("---startup application---")
    models.Base.metadata.create_all(bind=engine)

    with Session(engine) as db:
        seed_default_categories(db)


@app.on_event("shutdown")
def on_shutdown():
    logging.info("---shutdown application---")    


app.include_router(UserRouter, tags=["User"], prefix="/users")
app.include_router(AuthBackend, tags=["Authentication"])
app.include_router(TransactionRouter, tags=["Transaction"], prefix="/transactions")
app.include_router(CategoryRouter, tags=["Category"], prefix="/categories")
app.include_router(SavingsRouter, tags=["Savings"], prefix="/savings")
app.include_router(ReportRouter, tags=["Report"], prefix="/reports")
