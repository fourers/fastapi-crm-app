from functools import cache

from authlib.integrations.httpx_client import OAuth2Client

from app.config.keycloak import settings
from keycloak import KeycloakAdmin, KeycloakOpenIDConnection


@cache
def _get_admin_client():
    connection = KeycloakOpenIDConnection(
        server_url=settings.server_url,
        username=settings.admin_username,
        password=settings.admin_password,
        realm_name=settings.realm,
        user_realm_name="master",  # admin realm
        client_id="admin-cli",
    )
    return KeycloakAdmin(connection=connection)


def create_user(
    username: str, email: str | None, first_name: str | None, last_name: str | None
) -> str:
    client = _get_admin_client()
    user_payload = {
        "username": username,
        "email": email,
        "firstName": first_name,
        "lastName": last_name,
        "enabled": True,
        "credentials": [
            {
                "type": "password",
                "value": "password",
            }
        ],
    }
    return client.create_user(user_payload, exist_ok=False)


def delete_user(username: str):
    client = _get_admin_client()
    client.delete_user(user_id=username)


@cache
def get_oauth2_client() -> OAuth2Client:
    return OAuth2Client(
        settings.client_id,
        settings.client_secret,
    )
