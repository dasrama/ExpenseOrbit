from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app.schemas.auth import Token
from sqlalchemy.orm import Session
from app.utils import hash
from app.models import User
from app.database import get_db
from app.auth.oauth2 import create_access_token 

"""OAuth2PasswordRequestForm expects:
    username: {username}
    password: {password}"""

router = APIRouter()


@router.post("/login", response_model=Token)
def login(user_credentials : OAuth2PasswordRequestForm = Depends(), db : Session= Depends(get_db)):
    user = db.query(User).filter(user_credentials.username == User.email).first()
     
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Invalid User Credentials")
    
    if not hash.verify(plain_password= user_credentials.password,hashed_password= user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    access_token = create_access_token(data= {"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
    
