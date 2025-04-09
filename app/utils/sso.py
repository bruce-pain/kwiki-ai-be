from starlette.config import Config
from authlib.integrations.starlette_client import OAuth

from app.core.config import settings


# Initialize OAuth with the configuration settings
config_data = {
    "GOOGLE_CLIENT_ID": settings.GOOGLE_CLIENT_ID,
    "GOOGLE_CLIENT_SECRET": settings.GOOGLE_CLIENT_SECRET,
}

starlette_config = Config(environ=config_data)
oauth = OAuth(starlette_config)

# Register the Google OAuth provider
oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid profile email"},
)
