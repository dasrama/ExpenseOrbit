import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError, PyJWTError
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas.auth import Token, TokenData
from app.config import Settings


settings = Settings()

oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")

# SECRET KEY
# ALGORITHM
# ACCESS_TOKEN_EXPIRY_MINUTES

def create_access_token(data: dict) -> Token:
    # provided a copy of data to work on without changing the actual data
    to_encode = data.copy()
    expiry = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    # added extra information by adding to the existing data
    to_encode.update({"exp": expiry})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credential_exception) -> TokenData:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        id: str = payload.get("user_id")

        if not id:
            raise credential_exception

        token_data = TokenData(id=id) 
        return token_data
    except PyJWTError:
        raise credential_exception
    
    
def get_current_user(token: str = Depends(oauth_scheme), db: Session = Depends(get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credential_exception)
    current_user = db.query(User).filter(User.id == token.id).first()

    return current_user
