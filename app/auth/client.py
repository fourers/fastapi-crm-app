from functools import cache

import jwt
from async_lru import alru_cache
from authlib.integrations.starlette_client import OAuth, StarletteOAuth2App
from jwt import PyJWKClient

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


@alru_cache
async def _get_jwk_keys() -> PyJWKClient:
    metadata = await get_oauth_client().load_server_metadata()
    endpoint = metadata["jwks_uri"]
    return PyJWKClient(endpoint)


async def validate_jwt(token: str) -> None:
    jwk_keys = await _get_jwk_keys()
    jwt.decode(
        token,
        key=jwk_keys.get_signing_key_from_jwt(token),
        algorithms=["RS256"],
        options={
            "require": ["iss", "aud", "exp"],
            "verify_iss": True,
            "verify_aud": True,
            "verify_exp": True,
        },
        issuer=f"{settings.server_url}/realms/{settings.realm}",
        audience=settings.client_id,
    )
