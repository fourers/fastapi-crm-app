import shlex

import click
from dotenv import load_dotenv
from hvac import Client


@click.command()
@click.argument("user", default="admin", type=click.STRING)
def lookup_creds(user: str) -> None:
    client = Client()
    creds = client.secrets.kv.v2.read_secret_version(
        path=f"myapp/{user}", raise_on_deleted_version=True
    )["data"]["data"]
    postgres_creds = {
        "PGHOST": creds["host"],
        "PGPORT": creds["port"],
        "PGDATABASE": creds["database"],
        "PGUSER": creds["username"],
        "PGPASSWORD": creds["password"]
    }
    for k, v in postgres_creds.items():
        click.echo(f"export {k}={shlex.quote(v)}")


if __name__ == "__main__":
    load_dotenv()
    lookup_creds()
