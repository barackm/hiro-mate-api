from fastapi import APIRouter, Depends, Query, HTTPException, Request
from sqlalchemy.orm import Session
from app.db.database import get_db

router = APIRouter()

from fastapi.responses import RedirectResponse
from fastapi import APIRouter, Request
from app.modules.auth.service import oauth
from app.modules.users.service import create_user_from_google
from app.core.config import settings

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
        print("Token received:", token)
        if not token:
            raise ValueError("Failed to retrieve access token, token is None.")

        user_info = token.get("userinfo")
        print("User Info (from token):", user_info)

        if not user_info:
            user_info = await oauth.google.parse_id_token(request, token)
            print("User Info (from ID token):", user_info)
        first_name = user_info.get("given_name")
        last_name = user_info.get("family_name")
        email = user_info.get("email")
        sub = user_info.get("sub")
        user_info = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "sub": sub,
        }

        user = create_user_from_google(db, user_info)

        print("User:", user)

        return RedirectResponse(url=settings.FRONTEND_URL)

    except Exception as e:
        print("Error during Google callback:", e)
        return {"error": str(e)}


# @router.get("/login/facebook")
# async def login_via_facebook(request: Request):
#     redirect_uri = settings.FACEBOOK_REDIRECT_URI
#     print("Redirect URI:", redirect_uri)

#     return await oauth.facebook.authorize_redirect(request, redirect_uri)


# @router.get("/facebook/callback")
# async def facebook_callback(request: Request):
#     try:
#         token = await oauth.facebook.authorize_access_token(request)

#         user_info_response = await oauth.facebook.get(
#             "https://graph.facebook.com/me?fields=id,name,email", token=token
#         )
#         user_data = user_info_response.json()

#         print("User Data from Facebook:", user_data)

#         return {"user_info": user_data}

#     except Exception as e:
#         print("Error during Facebook callback:", e)
#         return {"error": str(e)}
