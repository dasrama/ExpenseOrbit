import os
from dotenv import load_dotenv

class Config:
    load_dotenv("discord_bot/.env") 

    @staticmethod
    def get(key: str, default=None, required: bool = False) -> str:
        value = os.getenv(key, default)
        if required and not value:
            raise ValueError(f"Missing required environment variable: {key}")
        return value

    CLIENT_ID = get("CLIENT_ID", required=True)
    CLIENT_SECRET = get("CLIENT_SECRET", required=True)
    REDIRECT_URI = get("REDIRECT_URI", required=True)
    GUILD_ID = get("GUILD_ID", required=True)
    API_URL = get("API_URL", required=True)
    TOKEN = get("TOKEN", required=True)