from app.utils.vault import get_secret


class Settings:
    @property
    def host(self):
        creds = get_secret("myapp/redis")
        return creds["host"]

    @property
    def port(self):
        creds = get_secret("myapp/redis")
        return creds["port"]

    @property
    def password(self):
        creds = get_secret("myapp/redis")
        return creds["password"]


settings = Settings()
