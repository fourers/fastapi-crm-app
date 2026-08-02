import os
from functools import cache

from app.utils.vault import get_secret
from keycloak import KeycloakAdmin, KeycloakOpenIDConnection


class Settings:
    @property
    def server_url(self):
        return os.environ["KC_URL"]

    @property
    def realm(self):
        return os.environ["KC_REALM"]

    @property
    def client_id(self):
        return os.environ["KC_CLIENT_ID"]

    @property
    def redirect_uri(self):
        return os.environ["KC_REDIRECT_URI"]


settings = Settings()


@cache
def get_admin_client():
    creds = get_secret("myapp/keycloak_admin")
    connection = KeycloakOpenIDConnection(
        server_url=settings.server_url,
        username=creds["username"],
        password=creds["password"],
        realm_name=settings.realm,
        user_realm_name="master",  # admin realm
        client_id="admin-cli",
    )

    return KeycloakAdmin(connection=connection)


def create_user(
    username: str, email: str | None, first_name: str | None, last_name: str | None
) -> str:
    client = get_admin_client()
    user_payload = {
        "username": username,
        "email": email or "",
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
    client = get_admin_client()
    client.delete_user(user_id=username)
