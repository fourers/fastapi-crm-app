import os


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
        pguser = os.environ["PGUSER"]
        pgpassword = os.environ["PGPASSWORD"]
        return self.generate_database_url(pguser, pgpassword)

    @property
    def admin_database_url(self):
        pguser = os.environ["ADMIN_PGUSER"]
        pgpassword = os.environ["ADMIN_PGPASSWORD"]
        return self.generate_database_url(pguser, pgpassword)


settings = Settings()
