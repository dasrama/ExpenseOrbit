from fastapi import FastAPI

from app.routers.auth import router as AuthBackend
from app.routers.user import router as UserRouter
from app import models
from app.database import engine


# will create all the corresponding tables in the database based on models defined in model.py .
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(UserRouter, tags=["User"], prefix="/user")
app.include_router(AuthBackend, tags=["Authentication"])
