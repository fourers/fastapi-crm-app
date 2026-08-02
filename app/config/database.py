import os

from app.utils.vault import get_secret


class Settings:
    @staticmethod
    def generate_database_url(pguser: str, pgpassword: str):
        pghost = os.environ["PGHOST"]
        pgport = os.environ["PGPORT"]
        pgdatabase = os.environ["PGDATABASE"]
        return (
            f"postgresql+psycopg://{pguser}:{pgpassword}@{pghost}:{pgport}/{pgdatabase}"
        )

    @property
    def database_url(self):
        app_user_creds = get_secret("myapp/app_user")
        return self.generate_database_url(
            app_user_creds["username"], app_user_creds["password"]
        )

    @property
    def admin_database_url(self):
        app_admin_creds = get_secret("myapp/app_admin")
        return self.generate_database_url(
            app_admin_creds["username"], app_admin_creds["password"]
        )


settings = Settings()
