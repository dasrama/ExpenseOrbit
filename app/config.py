from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    #JWT
    SECRET_KEY : str
    ALGORITHM : str
    ACCESS_TOKEN_EXPIRE_MINUTES : int 

    #DATABASE
    DATABASE_HOST: str
    DATABASE_PORT: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str

    class Config:
        env_file = ".env"

