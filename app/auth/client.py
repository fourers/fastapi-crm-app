from functools import cache

from authlib.integrations.starlette_client import OAuth, StarletteOAuth2App

from app.config.keycloak import settings


@cache
def get_oauth_client() -> StarletteOAuth2App:
    oauth = OAuth()
    oauth.register(
        name="keycloak",
        client_id=settings.client_id,
        client_secret=settings.client_secret,
        server_metadata_url=(
            f"{settings.server_url}/realms/{settings.realm}/.well-known/openid-configuration"
        ),
        client_kwargs={
            "scope": "openid profile email",
            "code_challenge_method": "S256",
        },
    )
    return oauth.create_client("keycloak")
