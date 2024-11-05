from fastapi import HTTPException, Depends
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from app.core.config import settings
from sqlalchemy.orm import Session
from app.db.database import get_db
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timezone, timedelta
from app.modules.users.model import User
import jwt as pyjwt


security = HTTPBearer()


config = Config(".env")
oauth = OAuth()

oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

oauth.register(
    name="facebook",
    client_id=settings.FACEBOOK_CLIENT_ID,
    client_secret=settings.FACEBOOK_CLIENT_SECRET,
    authorize_url="https://www.facebook.com/v11.0/dialog/oauth",
    access_token_url="https://graph.facebook.com/v11.0/oauth/access_token",
    client_kwargs={"scope": "email public_profile"},
)


def generate_refresh_token(user):
    payload = {
        "sub": str(user.id),
        "type": "refresh",
        "exp": datetime.now(timezone.utc)
        + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    }
    token = pyjwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token


def generate_access_token(user):
    payload = {
        "sub": str(user.id),
        "email": user.email,
        "provider": user.provider,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "exp": datetime.now(timezone.utc)
        + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    token = pyjwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token


def refresh_token_service(
    db: Session,
    refresh_token: str,
):
    try:
        payload = pyjwt.decode(refresh_token, settings.SECRET_KEY, algorithms=["HS256"])
        if payload["type"] != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")

        user_id = payload["sub"]
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        access_token = generate_access_token(user)
        return access_token

    except pyjwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except pyjwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def verify_access_token(
    token: str,
    db: Session = Depends(get_db),
):
    try:
        payload = pyjwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    except pyjwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Access token expired")
    except pyjwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
