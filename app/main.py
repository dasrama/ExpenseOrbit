from fastapi import FastAPI
from sqlalchemy.orm import Session

from app.routers.auth import router as AuthBackend
from app.routers.user import router as UserRouter
from app.routers.transaction import router as TransactionRouter
from app import models
from app.database import engine
from app.models import seed_default_categories


# will create all the corresponding tables in the database based on models defined in model.py .
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.on_event("startup")
def on_startup():
    models.Base.metadata.create_all(bind=engine)

    with Session(engine) as db:
        seed_default_categories(db)


app.include_router(UserRouter, tags=["User"], prefix="/user")
app.include_router(AuthBackend, tags=["Authentication"])
app.include_router(TransactionRouter, tags=["Transaction"], prefix="/transaction")
