import os

from app.utils.vault import get_secret


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

    @property
    def admin_username(self):
        creds = get_secret("myapp/keycloak_admin")
        return creds["username"]

    @property
    def admin_password(self):
        creds = get_secret("myapp/keycloak_admin")
        return creds["password"]


settings = Settings()
