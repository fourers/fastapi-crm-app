import os


class Settings:
    @property
    def database_url(self):
        pghost = os.environ["PGHOST"]
        pgport = os.environ["PGPORT"]
        pguser = os.environ["PGUSER"]
        pgpassword = os.environ["PGPASSWORD"]
        pgdatabase = os.environ["PGDATABASE"]

        return (
            f"postgresql+psycopg://{pguser}:{pgpassword}@{pghost}:{pgport}/{pgdatabase}"
        )


settings = Settings()
