import httpx
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import urllib.parse

from app.models import User
from app.database import get_db
from app.auth.oauth2 import create_access_token
from discord_bot.config import Config


router = APIRouter()

@router.get("/auth/callback")
async def discord_auth_callback(request: Request, db: Session = Depends(get_db)):
    code = request.query_params.get("code")

    if not code:
        raise HTTPException(status_code=400, detail="Authorization code not provided")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://discord.com/api/oauth2/token",
            data={
                "client_id": Config.CLIENT_ID,
                "client_secret": Config.CLIENT_SECRET,
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": Config.REDIRECT_URI
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        data = response.json()

    print("data: ", data)    
    
    if "access_token" not in data:
        raise HTTPException(status_code=400, detail="Failed to obtain access token")

    access_token = data["access_token"]

    async with httpx.AsyncClient() as client:
        user_response = await client.get(
            "https://discord.com/api/users/@me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        user_data = user_response.json()

    discord_id = user_data["id"]
    
    username = user_data["username"] # to be used later

    user = db.query(User).filter(User.discord_id == discord_id).first()

    if not user:
        # If user does not exist, create a new entry with a random email
        user = User(discord_id=discord_id)
        db.add(user)
        db.commit()
        db.refresh(user)

    jwt_token = create_access_token({"user_id": user.id})
    encoded_token = urllib.parse.quote(jwt_token)
    bot_command_url = f"https://discord.com/channels/{Config.GUILD_ID}?jwt_token={encoded_token}"

    return RedirectResponse(bot_command_url)

    #return {"message": "Discord login successful!", "jwt_token": jwt_token, "user_id": user.id}


