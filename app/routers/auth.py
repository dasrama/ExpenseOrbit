from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from .. import database, schemas
from sqlalchemy.orm import Session
from .. import models, utils
from app.auth.oauth2 import create_access_token 

"""OAuth2PasswordRequestForm expects:
    username: {username}
    password: {password}"""

router = APIRouter()


@router.post("/login", response_model=schemas.Token)
def login(user_credentials : OAuth2PasswordRequestForm = Depends(), db : Session= Depends(database.get_db)):
    user = db.query(models.User).filter(user_credentials.username == models.User.email).first()
     
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "invalid user credentials")
    
    if not utils.verify(plain_password= user_credentials.password,hashed_password= user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials")

    access_token = create_access_token(data= {"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
    
