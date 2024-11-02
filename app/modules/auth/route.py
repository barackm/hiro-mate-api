from fastapi import APIRouter

router = APIRouter()

from fastapi.responses import RedirectResponse
from fastapi import APIRouter, Request
from app.modules.auth.service import oauth
from app.core.config import settings

router = APIRouter()


@router.get("/login/google")
async def login_via_google(request: Request):
    redirect_uri = settings.GOOGLE_REDIRECT_URI
    print(redirect_uri)
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback")
async def google_callback(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
        print("Token received:", token)
        if not token:
            raise ValueError("Failed to retrieve access token, token is None.")

        user_info = token.get("userinfo")
        print("User Info (from token):", user_info)

        if not user_info:
            user_info = await oauth.google.parse_id_token(request, token)
            print("User Info (from ID token):", user_info)

        return RedirectResponse(url=settings.FRONTEND_URL)

    except Exception as e:
        print("Error during Google callback:", e)
        return {"error": str(e)}
