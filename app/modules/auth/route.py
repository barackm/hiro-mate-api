from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from app.db.database import get_db

router = APIRouter()

from fastapi import APIRouter, Request
from app.modules.auth.service import oauth
from app.modules.users.service import create_user_from_google
from app.core.config import settings
from .service import (
    generate_access_token,
    refresh_token_service,
    generate_refresh_token,
)

router = APIRouter()


@router.get("/login/google")
async def login_via_google(request: Request):
    redirect_uri = settings.GOOGLE_REDIRECT_URI
    print(redirect_uri)
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
        if not token:
            raise ValueError("Failed to retrieve access token, token is None.")

        user_info = token.get("userinfo")
        first_name = user_info.get("given_name")
        last_name = user_info.get("family_name")
        email = user_info.get("email")
        sub = user_info.get("sub")
        user_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "sub": sub,
        }

        user = create_user_from_google(db, user_data)

        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)

        redirect_to_path = request.query_params.get("redirect_to", "/")
        redirect_url = (
            f"{settings.FRONTEND_URL}{redirect_to_path}?access_token={access_token}"
        )

        response = RedirectResponse(url=redirect_url)
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            max_age=60 * 60 * 24 * settings.REFRESH_TOKEN_EXPIRE_DAYS,
            samesite="Lax",
        )
        return response

    except Exception as e:
        print("Error during Google callback:", e)
        return {"error": str(e)}


@router.post("/refresh")
async def refresh_token(request: Request, db: Session = Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=403, detail="Refresh token missing")

    access_token = refresh_token_service(refresh_token, db)
    return {"access_token": access_token}
