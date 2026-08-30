import os

from app.utils.vault import get_secret


class Settings:
    @property
    def server_url(self):
        return os.environ["KC_HOSTNAME"].rstrip("/")

    @property
    def realm(self):
        return os.environ["KC_REALM"]

    @property
    def client_id(self):
        creds = get_secret("myapp/keycloak_client")
        return creds["client_id"]

    @property
    def client_secret(self):
        creds = get_secret("myapp/keycloak_client")
        return creds["client_secret"]

    @property
    def admin_username(self):
        creds = get_secret("myapp/keycloak_admin")
        return creds["username"]

    @property
    def admin_password(self):
        creds = get_secret("myapp/keycloak_admin")
        return creds["password"]


settings = Settings()
