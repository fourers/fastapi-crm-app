from app.utils.vault import get_secret


class Settings:
    @staticmethod
    def generate_database_url(credentials: dict[str, str]):
        host = credentials["host"]
        port = credentials["port"]
        database = credentials["database"]
        username = credentials["username"]
        password = credentials["password"]
        return f"postgresql+psycopg://{username}:{password}@{host}:{port}/{database}"

    @property
    def database_url(self):
        return self.generate_database_url(get_secret("myapp/app_user"))

    @property
    def admin_database_url(self):
        return self.generate_database_url(get_secret("myapp/app_admin"))


settings = Settings()
