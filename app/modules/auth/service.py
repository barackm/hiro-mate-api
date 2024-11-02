from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from app.core.config import settings

config = Config(".env")
oauth = OAuth()

# Register Google OAuth client with the metadata URL
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
