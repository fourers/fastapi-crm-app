import os

from app.utils.vault import get_secret


class Settings:
    @property
    def host(self):
        return os.environ["REDIS_HOST"]

    @property
    def port(self):
        return os.environ["REDIS_PORT"]

    @property
    def password(self):
        creds = get_secret("myapp/redis")
        return creds["password"]


settings = Settings()
